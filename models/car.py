class Car:
    def __init__(self, car_id, brand, model, price_per_day, seating_capacity, available=True):
        self.car_id = car_id
        self.brand = brand
        self.model = model
        self.price_per_day = price_per_day
        self.seating_capacity = seating_capacity
        self.available = available

    def __str__(self):
        status = "Available" if self.available else "Rented"
        return f"{self.car_id}: {self.brand} {self.model} - ₹{self.price_per_day}/day, Seats: {self.seating_capacity}, {status}"

    @staticmethod
    def from_dict(data):
        return Car(
            car_id=data["car_id"],
            brand=data["brand"],
            model=data["model"],
            price_per_day=data["price_per_day"],
            seating_capacity=data["seating_capacity"],
            available=data.get("available", True)
        )

    def to_dict(self):
        return {
            "car_id": self.car_id,
            "brand": self.brand,
            "model": self.model,
            "price_per_day": self.price_per_day,
            "seating_capacity": self.seating_capacity,
            "available": self.available
        }
