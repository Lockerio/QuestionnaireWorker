from app.datetime_converter import DatetimeConverter


class MovementPreparer:
    def __init__(self):
        self.places_types = {
            "Дом": [
                'дом - место жительства'
            ],
            "Работа": [
                'работа - служебная поездка',
                'работа / рабочее место'
            ],
            "Учеба": [
                'университет / институт',
                'школа',
                'колледж / техникум / училище'
            ]
        }

    def get_movement_data(self, raw_movement_data, movement_date, person_id):
        movement_data = {
            "movement_date": movement_date, "person_id": person_id,
            "week_day": DatetimeConverter.date_to_weekday(movement_date),
            "departure_place_type": self.get_key_by_value(raw_movement_data["departurePlace"]),
            "arrival_place_type": self.get_key_by_value(raw_movement_data["arrivalPlace"]),
            "departure_time": DatetimeConverter.time_to_hours(raw_movement_data["departureTime"]),
            "arrival_time": DatetimeConverter.time_to_hours(raw_movement_data["arrivalTime"]),
            "departure_lat": raw_movement_data["coordinatesDepartureAddress"]["coordinates"][0],
            "departure_lon": raw_movement_data["coordinatesDepartureAddress"]["coordinates"][1],
            "arrival_lat": raw_movement_data["coordinatesArrivalAddress"]["coordinates"][0],
            "arrival_lon": raw_movement_data["coordinatesArrivalAddress"]["coordinates"][1]
        }

        return movement_data

    def get_key_by_value(self, value):
        for key, values in self.places_types.items():
            if value in values:
                return key
        return "Прочее"
