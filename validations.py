from config import CONFIG
import models


def check_date(date_string):
    """checks user date string is in correct format for parsing to a datetime object"""
    failure_message = CONFIG['date_check_failure_msg']
    try:
        date_time_obj = models.datetime.datetime.strptime(
            date_string, CONFIG['date_string_format']
        )
    except ValueError:
        return failure_message
    else:
        return date_time_obj


def check_time(time_string):
    """checks the user has entered a string that contains a character that can be parsed to int"""
    failure_message = CONFIG['time_check_failure_msg']
    try:
        minutes_int = int(time_string)
    except ValueError:
        return failure_message
    else:
        return minutes_int


def check_dates(date_string1, date_string2):
    """checks that the user makes correctly formatted date entries for date range search,
     using check_date() and orders the dates correctly"""
    dt_obj1 = check_date(date_string1)
    dt_obj2 = check_date(date_string2)
    failures = []
    if isinstance(dt_obj1, models.datetime.datetime) and isinstance(dt_obj2, models.datetime.datetime):
        if dt_obj1 <= dt_obj2:
            return dt_obj1, dt_obj2
        else:
            return dt_obj2, dt_obj1
    elif isinstance(dt_obj1, str) and isinstance(dt_obj2, models.datetime.datetime):
        dt_obj1 = 'start ' + dt_obj1
        failures.append(dt_obj1)
        failures.append(dt_obj2)
    elif isinstance(dt_obj2, str) and isinstance(dt_obj1, models.datetime.datetime):
        dt_obj2 = 'end ' + dt_obj2
        failures.append(dt_obj1)
        failures.append(dt_obj2)
    else:
        dt_obj1 = 'start ' + dt_obj1
        dt_obj2 = 'end ' + dt_obj2
        failures.append(dt_obj1)
        failures.append(dt_obj2)
    return failures