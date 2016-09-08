from django.conf.urls import url
from schedule.views import ScheduleView, ScheduleDetailView

urlpatterns = [
    url(r'^$', ScheduleView.as_view(), name='schedule'),
    url(r'^(?P<id>\w+)?$', ScheduleDetailView.as_view(), name='scheduleDetail')
]