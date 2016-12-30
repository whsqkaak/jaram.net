from django.conf.urls import url
from schedule.views import ScheduleView, EventView, ScheduleApiView, DailyScheduleView

urlpatterns = [
    url(r'^day/?$', DailyScheduleView.as_view(), name='daily_schedule'),
    url(r'^$', ScheduleView.as_view(), name='schedule'),
    url(r'^api/schedule/?$', ScheduleApiView.as_view(), name='schedule_api_user'),
    url(r'^(?P<id>\w+)?$', EventView.as_view(), name='event')
]