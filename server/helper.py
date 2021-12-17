"""
helper
"""

import datetime as dt

def flatten_json(original_json):
    """
    flattens json object

    :param json y: json object to flatten
    :return json out: flattened y
    """
    out = {}

    def flatten(potential_json, name=''):
        """
        flatten inner method
        """
        if isinstance(potential_json, dict):
            for key in potential_json:
                flatten(potential_json[key], name + key + '_')
        elif isinstance(potential_json, list):
            i = 0
            for key in potential_json:
                flatten(key, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = potential_json

    flatten(original_json)
    return out

def convert_epoch_milliseconds_to_datetime_string(time_in_millis):
    """
    convert epoch milliseconds to datetime

    :param int time_in_millis: time in millis
    :return datetime: datetime form of millis
    """
    return dt.datetime.fromtimestamp(time_in_millis / 1000.0).strftime("%Y-%m-%d %H:%M:%S")

def check_date_format(date_str):
    """
    check date format

    :param string date_str: date
    :return bool datetime: whether inputted date is in format "%Y-%m-%d"
    """
    date_format = "%Y-%m-%d"
    try:
        dt.datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False

def check_date_format_months(date_str):
    """
    check date format for months

    :param string date_str: date
    :return bool datetime: whether inputted date is in format "%Y-%m"
    """
    date_format = "%Y-%m"
    try:
        dt.datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False

def check_date_format_years(date_str):
    """
    check date format for years

    :param string date_str: date
    :return bool datetime: whether inputted date is in format "%Y"
    """
    date_format = "%Y"
    try:
        dt.datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False

def get_todays_date_str():
    """
    get today's date
    return string: today's date in '%Y-%m-%d'
    """
    return dt.datetime.today().strftime('%Y-%m-%d')

def is_month_in_date_range(year, month, from_year, to_year, from_month, to_month):
    """
    check if month is within a date month
    """
    if from_year == to_year:
        if (year == from_year) and (from_month <= month <= to_month):
            return True
    elif (year == from_year) and (month >= from_month):
        return True
    elif (year == to_year) and (month <= to_month):
        return True
    return False

def is_year_in_date_range(year, from_year, to_year):
    """
    check if year is within a date year
    """
    if from_year <= year <= to_year:
        return True
    return False
