from models.user import User

class Customer(User):
    def __init__(self, username, password, first_name, last_name, address, balance=0):
        super().__init__(username, password, first_name, last_name, address, balance)
        self.role = "customer"
        self.rental_history = []
        self.current_rental = None

    def rent_car(self, car, start_date, end_date):
        if self.current_rental:
            print("You already have a car rented.")
            return False
        if not car.available:
            print("Car is not available.")
            return False
        total_days = (end_date - start_date).days
        total_cost = total_days * car.price_per_day
        if self.balance < total_cost:
            print("Insufficient balance.")
            return False
        self.balance -= total_cost
        self.current_rental = {
            "car": car,
            "start": start_date,
            "end": end_date,
            "cost": total_cost
        }
        car.available = False
        print(f"Car rented successfully for {total_days} days. ₹{total_cost} deducted.")
        return True

    def return_car(self):
        if not self.current_rental:
            print("No car to return.")
            return
        self.rental_history.append(self.current_rental)
        self.current_rental["car"].available = True
        self.current_rental = None
        print("Car returned successfully.")

    def show_rental_history(self):
        if not self.rental_history:
            print("No rental history.")
            return
        for rental in self.rental_history:
            car = rental["car"]
            print(f"{car.brand} {car.model} | {rental['start']} to {rental['end']} | ₹{rental['cost']}")

    @classmethod
    def from_dict(cls, data):
        customer = cls(
            username=data['username'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            address=data['address'],
            balance=data.get('balance', 0)
        )
        return customer

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
