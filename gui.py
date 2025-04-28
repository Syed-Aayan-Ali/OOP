import tkinter as tk
from tkinter import messagebox, ttk
from rental_system import RentalSystem
from datetime import date

class CarRentalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Car Rental System")
        self.root.geometry("800x600")
        self.system = RentalSystem()
        self.logged_in_user = None

        self.init_main_screen()

    def init_main_screen(self):
        self.clear_frame()
        tk.Label(self.root, text="Welcome to Car Rental System", font=("Arial", 20)).pack(pady=20)

        tk.Button(self.root, text="Login", width=20, command=self.login_screen).pack(pady=10)
        tk.Button(self.root, text="Sign Up", width=20, command=self.signup_screen).pack(pady=10)

    def signup_screen(self):
        self.clear_frame()
        tk.Label(self.root, text="Sign Up", font=("Arial", 16)).pack(pady=10)

        entries = {}
        fields = ["Username", "Password", "First Name", "Last Name", "Address", "Balance", "Role"]
        for field in fields:
            tk.Label(self.root, text=field).pack()
            entry = tk.Entry(self.root)
            entry.pack()
            entries[field.lower().replace(" ", "_")] = entry

        def submit():
            try:
                data = {key: entry.get() for key, entry in entries.items()}
                data['balance'] = float(data['balance'])
                self.system.signup(data)
                messagebox.showinfo("Success", "Account created successfully!")
                self.init_main_screen()
            except Exception as e:
                messagebox.showinfo("Failed", e)

        tk.Button(self.root, text="Submit", command=submit).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.init_main_screen).pack()

    def login_screen(self):
        self.clear_frame()
        tk.Label(self.root, text="Login", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        def login():
            username = username_entry.get()
            password = password_entry.get()
            success = self.system.login(username, password)
            if success:
                self.logged_in_user = self.system.logged_in_user
                if self.logged_in_user.role == "admin":
                    self.admin_dashboard()
                else:
                    self.customer_dashboard()
            else:
                messagebox.showerror("Error", "Invalid credentials")

        tk.Button(self.root, text="Login", command=login).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.init_main_screen).pack()

    def customer_dashboard(self):
        self.clear_frame()
        tk.Label(self.root, text=f"Welcome, {self.logged_in_user.first_name} (Customer)", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="View Available Cars", command=self.view_cars).pack(pady=5)
        tk.Button(self.root, text="View Rental History", command=self.view_rental_history).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.init_main_screen).pack(pady=5)

    def admin_dashboard(self):
        self.clear_frame()
        tk.Label(self.root, text=f"Welcome, {self.logged_in_user.first_name} (Admin)", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Add Car", command=self.add_car_screen).pack(pady=5)
        tk.Button(self.root, text="Remove Car", command=self.remove_car_screen).pack(pady=5)
        tk.Button(self.root, text="View Reserved Cars", command=self.view_reserved_cars).pack(pady=5)
        tk.Button(self.root, text="View Customer Rentals", command=self.view_customer_rentals).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.init_main_screen).pack(pady=5)

    def view_cars(self):
        self.clear_frame()
        tk.Label(self.root, text="Available Cars", font=("Arial", 14)).pack(pady=10)

        cars = self.system.display_available_cars()
        print('Available cars are:',cars)
        for car in cars:
            car_text = f"{car.car_id} - {car.brand} {car.model} - Rs. {car.price_per_day}/day"
            btn = tk.Button(self.root, text=car_text, command=lambda c=car: self.rent_car_screen(c))
            btn.pack(pady=2)

        tk.Button(self.root, text="Back", command=self.customer_dashboard).pack(pady=10)

    def rent_car_screen(self, car):
        self.clear_frame()
        tk.Label(self.root, text=f"Rent Car: {car.brand} {car.model}", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="Start Date (YYYY-MM-DD)").pack()
        start_entry = tk.Entry(self.root)
        start_entry.pack()

        tk.Label(self.root, text="End Date (YYYY-MM-DD)").pack()
        end_entry = tk.Entry(self.root)
        end_entry.pack()

        def confirm_rent():
            start = date.fromisoformat(start_entry.get())
            end = date.fromisoformat(end_entry.get())
            try:
                self.system.rent_car(self.logged_in_user, car.car_id, start, end)
                messagebox.showinfo("Success", "Car rented successfully!")
                self.customer_dashboard()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.root, text="Confirm", command=confirm_rent).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.view_cars).pack(pady=5)

    def view_rental_history(self):
        self.clear_frame()
        tk.Label(self.root, text="Rental History", font=("Arial", 14)).pack(pady=10)

        for rental in self.logged_in_user.rental_history:
            tk.Label(self.root, text=str(rental)).pack()

        tk.Button(self.root, text="Back", command=self.customer_dashboard).pack(pady=10)

    def add_car_screen(self):
        self.clear_frame()
        tk.Label(self.root, text="Add New Car", font=("Arial", 14)).pack(pady=10)

        entries = {}
        fields = ["Car ID", "Brand", "Model", "Price Per Day", "Seating Capacity"]
        for field in fields:
            tk.Label(self.root, text=field).pack()
            entry = tk.Entry(self.root)
            entry.pack()
            entries[field.lower().replace(" ", "_")] = entry

        def submit():
            try:
                self.system.admin_add_car(
                    entries["car_id"].get(),
                    entries["brand"].get(),
                    entries["model"].get(),
                    float(entries["price_per_day"].get()),
                    int(entries["seating_capacity"].get())
                )
                messagebox.showinfo("Success", "Car added successfully!")
                self.admin_dashboard()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.root, text="Add", command=submit).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.admin_dashboard).pack()

    def remove_car_screen(self):
        self.clear_frame()
        tk.Label(self.root, text="Remove Car", font=("Arial", 14)).pack(pady=10)

        for car in self.system.cars:
            if car.is_available:
                tk.Button(self.root, text=f"{car.car_id} - {car.brand} {car.model}",
                          command=lambda c=car: self.remove_car(c)).pack(pady=2)

        tk.Button(self.root, text="Back", command=self.admin_dashboard).pack(pady=10)

    def remove_car(self, car):
        self.system.admin_remove_car(car.car_id)
        messagebox.showinfo("Success", "Car removed successfully!")
        self.admin_dashboard()

    def view_reserved_cars(self):
        self.clear_frame()
        tk.Label(self.root, text="Reserved Cars", font=("Arial", 14)).pack(pady=10)

        reserved = [car for car in self.system.cars if not car.is_available]
        for car in reserved:
            tk.Label(self.root, text=f"{car.car_id} - {car.brand} {car.model}").pack()

        tk.Button(self.root, text="Back", command=self.admin_dashboard).pack(pady=10)

    def view_customer_rentals(self):
        self.clear_frame()
        tk.Label(self.root, text="Customer Rentals", font=("Arial", 14)).pack(pady=10)

        for user in self.system.users:
            if user.role == "customer" and user.rental_history:
                tk.Label(self.root, text=f"{user.username}:").pack()
                for rental in user.rental_history:
                    tk.Label(self.root, text=str(rental)).pack()

        tk.Button(self.root, text="Back", command=self.admin_dashboard).pack(pady=10)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = CarRentalGUI(root)
    root.mainloop()