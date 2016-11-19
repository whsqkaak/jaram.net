from django.conf.urls import url
from schedule.views import ScheduleView, EventView, ScheduleApiView

urlpatterns = [
    url(r'^$', ScheduleView.as_view(), name='schedule'),
    url(r'^api/schedule/?$', ScheduleApiView.as_view(), name='schedule_api_user'),
    url(r'^(?P<id>\w+)?$', EventView.as_view(), name='event')
]