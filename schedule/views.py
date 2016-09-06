from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime, date
from django.views.generic import TemplateView
from main.util import create_response
import calendar

from schedule.models import Event


class ScheduleView(TemplateView):
    template_name = 'schedule/calendar.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        today = date.today()
        year = today.year
        month = today.month
        response['new_calendar'] = calendar.monthcalendar(year, month)
        response['events'] = Event.objects.filter(
            start_date__range=(
                datetime(year, month, 1), datetime(year, month, calendar.monthrange(year, month)[1]))).order_by(
            '-start_date')
        return render(request, self.template_name, response)


class EventDetailView(TemplateView):
    template_name = ''

    def get(self, request, *args, **kwargs):
        response = create_response(request)

        return render(request, self.template_name, response)
