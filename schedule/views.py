from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.utils.datetime_safe import date
from django.views.generic import View, TemplateView
from main.util import create_response
from main.utils.calender import jaram_calendar
from main.models import Grade
from schedule.models import Event


class ScheduleView(TemplateView):
    template_name = 'schedule/calendar.html'

    def get(self, request, *args, **kwargs):
        if request.user.grade == Grade.objects.get(name='미승인'):
            return redirect('/main?warning=권한이 없습니다.')
        response = create_response(request)
        today = date.today()
        jaram_calendar(Event, today.year, today.month, response)
        return render(request, self.template_name, response)


class ScheduleApiView(View):
    template_name = 'jaram_calendar.html'

    def get(self, request, *args, **kwargs):
        response = dict()
        year = int(request.GET.get('y'))
        month = int(request.GET.get('m'))
        jaram_calendar(Event, year, month, response)
        return render(request, self.template_name, response)


class EventView(TemplateView):
    template_name = 'schedule/detail.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        if request.user.grade == Grade.objects.get(name='미승인'):
            return redirect('/main?warning=권한이 없습니다.')
        try:
            event = Event.objects.get(pk=kwargs.get('id'))
            response['event'] = event
        except ObjectDoesNotExist:
            return redirect('/main/?warning=잘못된 접근입니다.')
        return render(request, self.template_name, response)
