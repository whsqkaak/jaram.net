from board.views import PlayStormingView, SeminarView, EventReportView
from django.conf.urls import url

from main.views import IntroView

urlpatterns = [
    url(r'^playstorming$', PlayStormingView.as_view(), name='playstorming'),
    url(r'^seminar$', SeminarView.as_view(), name='seminar'),
    url(r'^event_report$', EventReportView.as_view(), name='event_report'),
]