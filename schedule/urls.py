from django.conf.urls import url
from schedule.views import ScheduleView

urlpatterns = [
    url(r'^$', ScheduleView.as_view(), name='schedule'),
]