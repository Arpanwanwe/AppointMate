import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import datetime
from tkcalendar import Calendar
from PIL import Image, ImageTk

class Appointment:
    def __init__(self, name, date, time, contact, email, reason, notes=""):
        self.name = name
        self.date = date
        self.time = time
        self.contact = contact
        self.email = email
        self.reason = reason
        self.notes = notes

    def __str__(self):
        return f"Name: {self.name}\nDate: {self.date}\nTime: {self.time}\nContact: {self.contact}\nEmail: {self.email}\nReason: {self.reason}\nNotes: {self.notes}"

class TimeChooser(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Choose Time")
        self.configure(bg="#f0f0f0")
        self.selected_time = tk.StringVar()

        tk.Label(self, text="Hour (0-23):", font=("Arial", 10), bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        self.hour_entry = tk.Entry(self, width=5)
        self.hour_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Minute (0-59):", font=("Arial", 10), bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
        self.minute_entry = tk.Entry(self, width=5)
        self.minute_entry.grid(row=1, column=1, padx=5, pady=5)

        select_button = tk.Button(self, text="Select Time", command=self.set_time, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        select_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.result = None

    def set_time(self):
        hour = self.hour_entry.get()
        minute = self.minute_entry.get()
        try:
            hour_int = int(hour)
            minute_int = int(minute)
            if 0 <= hour_int <= 23 and 0 <= minute_int <= 59:
                self.result = f"{hour_int:02d}:{minute_int:02d}"
                self.destroy()
            else:
                messagebox.showerror("Error", "Invalid hour or minute value.")
        except ValueError:
            messagebox.showerror("Error", "Please enter numeric values for hour and minute.")

    def get_time(self):
        self.wait_window()
        return self.result

class AppointmentManager(tk.Frame):
    def __init__(self, master, logo_path):
        super().__init__(master)
        self.master = master
        master.title("AppointMate - By Arpan")
        master.configure(bg="#e0f2f7")

        try:
            img = Image.open(logo_path)
            img = img.resize((100, 100))
            self.logo_img = ImageTk.PhotoImage(img)
            logo_label = tk.Label(master, image=self.logo_img, bg="#e0f2f7")
            logo_label.grid(row=0, column=0, columnspan=3, pady=10)
        except FileNotFoundError:
            messagebox.showerror("Error", "Logo file not found!")

        label_font = ("Arial", 12)
        button_font = ("Arial", 10, "bold")
        entry_font = ("Arial", 10)

        tk.Label(master, text="Name:", font=label_font, bg="#e0f2f7").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Label(master, text="Date:", font=label_font, bg="#e0f2f7").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        tk.Label(master, text="Time:", font=label_font, bg="#e0f2f7").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        tk.Label(master, text="Contact No.:", font=label_font, bg="#e0f2f7").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        tk.Label(master, text="Email:", font=label_font, bg="#e0f2f7").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        tk.Label(master, text="Reason:", font=label_font, bg="#e0f2f7").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        tk.Label(master, text="Notes:", font=label_font, bg="#e0f2f7").grid(row=7, column=0, padx=10, pady=5, sticky="w")

        self.name_entry = tk.Entry(master, font=entry_font)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.date_entry = tk.Entry(master, font=entry_font)
        self.date_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.time_entry = tk.Entry(master, font=entry_font)
        self.time_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        self.contact_entry = tk.Entry(master, font=entry_font)
        self.contact_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        self.email_entry = tk.Entry(master, font=entry_font)
        self.email_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

        self.reason_entry = tk.Entry(master, font=entry_font)
        self.reason_entry.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

        self.notes_entry = tk.Text(master, height=3, width=30, font=entry_font)
        self.notes_entry.grid(row=7, column=1, padx=10, pady=5, sticky="ew")

        self.calendar_button = tk.Button(master, text="Choose Date", command=self.show_calendar, bg="#2196F3", fg="white", font=button_font)
        self.calendar_button.grid(row=2, column=2, padx=5, pady=5)

        self.time_button = tk.Button(master, text="Choose Time", command=self.show_time_chooser, bg="#2196F3", fg="white", font=button_font)
        self.time_button.grid(row=3, column=2, padx=5, pady=5)

        add_button = tk.Button(master, text="Add Appointment", command=self.add_appointment, bg="#4CAF50", fg="white", font=button_font)
        add_button.grid(row=8, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

        view_button = tk.Button(master, text="View Appointments", command=self.view_appointments, bg="#008CBA", fg="white", font=button_font)
        view_button.grid(row=9, column=0, columnspan=3, pady=5, padx=10, sticky="ew")

        export_csv_button = tk.Button(master, text="Export to CSV", command=self.export_to_csv, bg="#ff9800", fg="white", font=button_font)
        export_csv_button.grid(row=10, column=0, columnspan=3, pady=5, padx=10, sticky="ew")

        logout_button = tk.Button(master, text="Logout", command=self.logout, bg="#f44336", fg="white", font=button_font)
        logout_button.grid(row=11, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

        self.appointments = []

    def logout(self):
        self.master.destroy()
        main()

    def show_calendar(self):
        top = tk.Toplevel(self.master)
        cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(pady=10, padx=10)
        tk.Button(top, text="Select Date", command=lambda: self.set_date(cal.get_date(), top), bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(pady=5)
        top.configure(bg="#f0f0f0")

    def set_date(self, date_str, calendar_window):
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, date_str)
        calendar_window.destroy()

    def show_time_chooser(self):
        time_dialog = TimeChooser(self.master)
        time_result = time_dialog.get_time()
        if time_result:
            self.time_entry.delete(0, tk.END)
            self.time_entry.insert(0, time_result)

    def check_overlap(self, new_date, new_time):
        for appt in self.appointments:
            if appt.date == new_date and appt.time == new_time:
                return True
        return False

    def add_appointment(self):
        name = self.name_entry.get()
        date_str = self.date_entry.get()
        time_str = self.time_entry.get()
        contact = self.contact_entry.get()
        email = self.email_entry.get()
        reason = self.reason_entry.get()
        notes = self.notes_entry.get("1.0", tk.END).strip()

        if not all([name, date_str, time_str]):
            messagebox.showerror("Error", "Name, Date, and Time cannot be empty.")
            return

        try:
            datetime.datetime.strptime(date_str, '%Y-%m-%d')
            datetime.datetime.strptime(time_str, '%H:%M')
        except ValueError:
            messagebox.showerror("Error", "Invalid Date or Time format. Please use %Y-%m-%d and HH:MM.")
            return

        if self.check_overlap(date_str, time_str):
            messagebox.showerror("Warning", "An appointment already exists at this date and time.")
            return

        appointment = Appointment(name, date_str, time_str, contact, email, reason, notes)
        self.appointments.append(appointment)
        messagebox.showinfo("Success", "Appointment added successfully!")
        self.clear_input_fields()

    def clear_input_fields(self):
        self.name_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.reason_entry.delete(0, tk.END)
        self.notes_entry.delete("1.0", tk.END)

    def view_appointments(self):
        if not self.appointments:
            messagebox.showinfo("Info", "No appointments scheduled yet.")
            return

        view_window = tk.Toplevel(self.master)
        view_window.title("Scheduled Appointments")
        view_window.configure(bg="#f0f0f0")

        text_area = tk.Text(view_window, height=15, width=70, font=("Arial", 10))
        text_area.pack(padx=10, pady=10)
        text_area.config(state=tk.DISABLED)

        all_appointments_text = "--- All Appointments ---\n\n"
        for i, appointment in enumerate(self.appointments):
            all_appointments_text += f"Appointment {i+1}:\n{appointment}\n\n"

        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, all_appointments_text)
        text_area.config(state=tk.DISABLED)

    def export_to_csv(self):
        if not self.appointments:
            messagebox.showinfo("Info", "No appointments to export.")
            return

        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if filepath:
            try:
                with open(filepath, 'w', newline='') as csvfile:
                    fieldnames = ['Name', 'Date', 'Time', 'Contact', 'Email', 'Reason', 'Notes']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for appt in self.appointments:
                        writer.writerow({
                            'Name': appt.name,
                            'Date': appt.date,
                            'Time': appt.time,
                            'Contact': appt.contact,
                            'Email': appt.email,
                            'Reason': appt.reason,
                            'Notes': appt.notes
                        })
                messagebox.showinfo("Success", f"Appointments exported to {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Error exporting to CSV: {e}")

class LoginWindow(tk.Tk):
    def __init__(self, logo_path):
        super().__init__()
        self.title("Login")
        self.configure(bg="#f0f0f0")
        self.app_manager = None
        self.logo_path = logo_path

        try:
            img = Image.open(self.logo_path)
            img = img.resize((100, 100))
            self.logo_img = ImageTk.PhotoImage(img)
            logo_label = tk.Label(self, image=self.logo_img, bg="#f0f0f0")
            logo_label.grid(row=0, column=0, columnspan=2, pady=10)
        except FileNotFoundError:
            messagebox.showerror("Error", "Logo file not found!")

        self.username_label = tk.Label(self, text="Username:", font=("Arial", 12), bg="#f0f0f0")
        self.username_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.username_entry = tk.Entry(self, font=("Arial", 12))
        self.username_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.password_label = tk.Label(self, text="Password:", font=("Arial", 12), bg="#f0f0f0")
        self.password_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.password_entry = tk.Entry(self, show="*", font=("Arial", 12))
        self.password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.login_button = tk.Button(self, text="Login", command=self.login, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.login_button.grid(row=3, column=0, columnspan=2, pady=20)

        self.grid_columnconfigure(1, weight=1)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "Admin" and password == "Admin":
            self.destroy()
            root = tk.Tk()
            self.app_manager = AppointmentManager(root, self.logo_path)
            root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

def main():
    logo_file = "AppointMate_Logo_WBG.png"
    login_window = LoginWindow(logo_file)
    login_window.mainloop()

if __name__ == "__main__":
    main()
