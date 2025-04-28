from datetime import date
from models.customer import Customer
from models.admin import Admin
from models.car import Car
from models.rental import Rental
from services.auth import AuthService
from services.car_service import CarService
from services.payment import PaymentService
from services.rental_service import RentalService
from services.file_saver import FileService


class RentalSystem:
    def __init__(self):
        self.users = FileService.load_users()
        self.cars = FileService.load_cars()
        self.logged_in_user = None

    def save_all(self):
        FileService.save_users(self.users)
        FileService.save_cars(self.cars)

    def signup(self, data):
        print("your data:",data)

        # GUI mode
        username = data['username']
        password = data['password']
        first_name = data['first_name']
        last_name = data['last_name']
        address = data['address']
        balance = data['balance']
        role = data['role']

        try:
            if role.lower() not in ['admin', 'customer']:
                print("Role should be Admin or Customer")
                raise Exception("Role should be Admin or Customer")
    
            user_data = {
            "username": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "address": address,
            "balance": balance
            }
    
            user = AuthService.signup(user_data, role=role)  # Pass role separately

            self.users.append(user)
            print(f"{role.capitalize()} account created successfully!")

        except Exception as e:
            print("Signup error:", e)
            raise Exception("Signup failed due to invalid role or data")
        
        import re  # Import regex module for pattern checking
        try:
            if len(password) < 6:
                raise Exception("Password must be at least 6 characters long.")
            if not re.search(r"[A-Z]", password):
                raise Exception("Password must contain at least one uppercase letter.")
            if not re.search(r"[0-9]", password):
                raise Exception("Password must contain at least one number.")
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                raise Exception("Password must contain at least one special character.")

            # Password is valid, continue with signup
            print("Password is valid!")

        except Exception as e:
            print("Signup error:", e)
            raise Exception("Invalid password format.")


        
        # try:
        #     if role not in ['Admin', 'admin', 'Customer', 'customer']:
        #         print("Role should be Admin or Customer")
        #         raise Exception("Role should be Admin or Customer")
        #     user = AuthService.signup({
        #         "username": username,
        #         "password": password,
        #         "first_name": first_name,
        #         "last_name": last_name,
        #         "address": address,
        #         "balance": balance,
        #         "role": role
        #     }, role=role)
        #     self.users.append(user)
        #     print(f"{role.capitalize()} account created successfully!")
        # except Exception as e:
        #     print("Signup error:", e)
        #     raise Exception("Role should be Admin  or Customer")
        
        # while True:
        #     try:
        #         balance = float(balance)  # Try converting to float
        #         print("Your balance is:", balance)
        #         break  # Exit the loop if successful
        #     except ValueError:
        #         print("Invalid input! Please enter a valid float number.")



    def login(self, username, password):
        print("\n--- Login ---")
        # username = input("Username: ")
        # password = input("Password: ")
        user = AuthService.login(username, password)
        if user:
            self.logged_in_user = user
            print(f"Welcome {user.first_name}!")
            return True
        else:
            print("Invalid login credentials.")
            return False

    def display_available_cars(self):
        available_cars = [car for car in self.cars if car.available]
        if not available_cars:
            print("No cars available.")
        else:
            for car in available_cars:
                print(f"{car.car_id}: {car.brand} {car.model} - ₹{car.price_per_day}/day, Seats: {car.seating_capacity}, Available")
    
        return available_cars  # <-- This is important!


    def rent_car(self):
        self.display_available_cars()
        car_id = input("Enter Car ID to rent: ")
        car = CarService.find_car_by_id(self.cars, car_id)

        if not car or not car.is_available:
            print("Invalid or unavailable car.")
            return

        try:
            start = date.fromisoformat(input("Start date (YYYY-MM-DD): "))
            end = date.fromisoformat(input("End date (YYYY-MM-DD): "))

            if not RentalService.is_valid_rental_period(start, end):
                print("Invalid rental period.")
                return

            cost = RentalService.calculate_total_cost(car.price_per_day, start, end)

            if PaymentService.process_payment(self.logged_in_user, cost):
                rental = Rental(car_id, start, end, cost)
                self.logged_in_user.rental_history.append(rental)
                car.is_available = False
                print("Car rented successfully.")
            else:
                print("Payment failed.")
        except Exception as e:
            print("Rental error:", e)

    def view_rental_history(self):
        print("\n--- Rental History ---")
        for rental in self.logged_in_user.rental_history:
            print(rental)

    def update_balance(self):
        amount = float(input("Enter amount to add: "))
        self.logged_in_user.balance += amount
        print(f"New balance: {self.logged_in_user.balance}")

    def admin_add_car(self,car_id,brand,model,price,seats,car):
        print("\n--- Add New Car ---")
        car_id = input("Car ID: ")
        brand = input("Brand: ")
        model = input("Model: ")
        price = float(input("Price per day: "))
        seats = int(input("Seating capacity: "))
        car = Car(car_id, brand, model, price, seats)
        CarService.add_car(self.cars, car)
        print("Car added successfully.")

    def admin_remove_car(self):
        car_id = input("Enter Car ID to remove: ")
        self.cars = CarService.remove_car(self.cars, car_id)
        print("Car removed.")

    def admin_update_price(self):
        car_id = input("Enter Car ID: ")
        car = CarService.find_car_by_id(self.cars, car_id)
        if car:
            new_price = float(input("Enter new price per day: "))
            car.price_per_day = new_price
            print("Price updated.")
        else:
            print("Car not found.")

    def admin_customer_report(self):
        print("\n--- All Customers & Their Rentals ---")
        for user in self.users:
            if isinstance(user, Customer):
                print(f"{user.username} - Balance: {user.balance}")
                for rental in user.rental_history:
                    print(f"   {rental}")

    def admin_reserved_cars_report(self):
        print("\n--- All Reserved Cars ---")
        for car in self.cars:
            if not car.is_available:
                print(car)

    def user_menu(self):
        while True:
            print("\n1. Rent a car\n2. View rental history\n3. Add balance\n4. Logout")
            choice = input("Choose: ")
            if choice == "1":
                self.rent_car()
            elif choice == "2":
                self.view_rental_history()
            elif choice == "3":
                self.update_balance()
            elif choice == "4":
                self.save_all()
                self.logged_in_user = None
                break
            else:
                print("Invalid choice.")

    def admin_menu(self):
        while True:
            print("\n1. Add car\n2. Remove car\n3. Change car price")
            print("4. View customer rental report\n5. View reserved cars\n6. Logout")
            choice = input("Choose: ")
            if choice == "1":
                self.admin_add_car()
            elif choice == "2":
                self.admin_remove_car()
            elif choice == "3":
                self.admin_update_price()
            elif choice == "4":
                self.admin_customer_report()
            elif choice == "5":
                self.admin_reserved_cars_report()
            elif choice == "6":
                self.save_all()
                self.logged_in_user = None
                break
            else:
                print("Invalid choice.")

    def main_menu(self):
        while True:
            print("\n--- Car Rental System ---")
            print("1. Login\n2. Signup\n3. Exit")
            choice = input("Choose: ")

            if choice == "1":
                if self.login():
                    if isinstance(self.logged_in_user, Admin):
                        self.admin_menu()
                    else:
                        self.user_menu()
            elif choice == "2":
                self.signup()
            elif choice == "3":
                self.save_all()
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
