from datetime import datetime


class DatetimeConverter:
    @staticmethod
    def time_to_hours(time_str):
        if ":" in time_str:
            hours, minutes = time_str.split(':')
            if minutes == "00":
                return int(hours)
            if hours == "23":
                return 0
            return int(hours) + 1
        else:
            return 14

    @staticmethod
    def date_to_weekday(date_string, date_format='%Y-%m-%d'):
        date_object = datetime.strptime(date_string, date_format)
        week_day = date_object.weekday()
        week_day_names = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
        day_of_week = week_day_names[week_day]
        return day_of_week
