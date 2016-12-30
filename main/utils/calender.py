import calendar

from django.utils.datetime_safe import datetime


def jaram_calendar(data, year, month, save_to=None):  # 일정, 년, 월, save_to
    (starting_weekday, num_of_days) = calendar.monthrange(year, month)
    calendar.setfirstweekday(calendar.SUNDAY)
    if save_to is not None:
        save_to['year'] = year
        save_to['month'] = month
        save_to['new_calendar'] = calendar.monthcalendar(year, month)
        events = data.objects.filter(
             start_date__range=(
                 datetime(year, month, 1), datetime(year, month, num_of_days))).order_by(
             '-start_date')
        save_to['events'] = events