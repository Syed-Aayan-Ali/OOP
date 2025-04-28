from datetime import date

class Rental:
    def __init__(self, car_id, start_date, end_date, cost):
        self.car_id = car_id
        self.start_date = start_date  # expected as date object
        self.end_date = end_date      # expected as date object
        self.cost = cost

    def to_dict(self):
        return {
            "car_id": self.car_id,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "cost": self.cost
        }

    @staticmethod
    def from_dict(data):
        return Rental(
            car_id=data["car_id"],
            start_date=date.fromisoformat(data["start_date"]),
            end_date=date.fromisoformat(data["end_date"]),
            cost=data["cost"]
        )

    def __str__(self):
        return f"Car ID: {self.car_id}, From: {self.start_date}, To: {self.end_date}, Cost: ₹{self.cost}"
