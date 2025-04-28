from models.car import Car

class CarService:
    @staticmethod
    def get_available_cars(car_list):
        return [car for car in car_list if car.available]

    @staticmethod
    def find_car_by_id(car_list, car_id):
        for car in car_list:
            if car.car_id == car_id:
                return car
        return None

    @staticmethod
    def add_car(car_list, new_car):
        car_list.append(new_car)

    @staticmethod
    def remove_car(car_list, car_id):
        return [car for car in car_list if car.car_id != car_id]
