from models.user import User
from models.customer import Customer

class Admin(User):
    def __init__(self, username, password, first_name, last_name, address, balance=0):
        super().__init__(username, password, first_name, last_name, address, balance)
        self.role = 'admin'

    def add_car(self, car_list, car):
        car_list.append(car)
        print(f"Car {car.car_id} added.")

    def remove_car(self, car_list, car_id):
        for car in car_list:
            if car.car_id == car_id:
                car_list.remove(car)
                print(f"Car {car_id} removed.")
                return
        print(f"Car {car_id} not found.")

    def change_car_price(self, car_list, car_id, new_price):
        for car in car_list:
            if car.car_id == car_id:
                car.price_per_day = new_price
                print(f"Updated price of {car_id} to ₹{new_price}.")
                return
        print(f"Car {car_id} not found.")

    def print_all_customers(self, customers):
        for user in customers:
            if isinstance(user, Customer):
                print(f"{user.username} - {user.first_name} {user.last_name}, Balance: ₹{user.balance}")
                if user.current_rental:
                    car = user.current_rental["car"]
                    print(f"  Renting: {car.brand} {car.model} ({car.car_id})")

    def print_reserved_cars(self, car_list):
        for car in car_list:
            if not car.available:
                print(f"{car.car_id} - {car.brand} {car.model}")

    @classmethod
    def from_dict(cls, data):
        return cls(
            username=data['username'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            address=data['address'],
            balance=data.get('balance', 0)
        )

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address,
            "balance": self.balance,
            "role": self.role
        }
