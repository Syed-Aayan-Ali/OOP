from datetime import date

class RentalService:
    @staticmethod
    def calculate_rental_days(start_date, end_date):
        return (end_date - start_date).days

    @staticmethod
    def calculate_total_cost(price_per_day, start_date, end_date):
        total_days = RentalService.calculate_rental_days(start_date, end_date)
        return total_days * price_per_day

    @staticmethod
    def is_valid_rental_period(start_date, end_date):
        return start_date < end_date and start_date >= date.today()
