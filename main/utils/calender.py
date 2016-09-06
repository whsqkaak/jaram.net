import calendar

from django.utils.datetime_safe import date


def jaram_calendar(data, year, month, save_to=None): #일정, 년, 월, save_to
    month_to_print = date(year, month)
    (starting_weekday, num_of_days) = calendar.monthrange(year, month)
