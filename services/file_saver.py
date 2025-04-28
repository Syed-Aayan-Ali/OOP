import json
from models.customer import Customer
from models.admin import Admin
from models.car import Car

class FileService:
    @staticmethod
    def load_users():
        try:
            with open("data/users.json", "r") as f:
                data = json.load(f)
                users = []
                for item in data:
                    if item.get("role") == "admin":
                        users.append(Admin.from_dict(item))
                    else:
                        users.append(Customer.from_dict(item))
                return users
        except FileNotFoundError:
            return []

    @staticmethod
    def save_users(users):
        with open("data/users.json", "w") as f:
            json.dump([u.to_dict() for u in users], f, indent=4)

    @staticmethod
    def load_cars():
        try:
            with open("data/cars.json", "r") as f:
                data = json.load(f)
                return [Car.from_dict(item) for item in data]
        except FileNotFoundError:
            return []

    @staticmethod
    def save_cars(cars):
        with open("data/cars.json", "w") as f:
            json.dump([car.to_dict() for car in cars], f, indent=4)
