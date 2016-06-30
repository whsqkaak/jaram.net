from board.views import PlayStormingView, SeminarView, EventReportView, SeminarListView, MakePostView
from django.conf.urls import url

from main.views import IntroView

urlpatterns = [
    url(r'^playstorming$', PlayStormingView.as_view(), name='playstorming'),
    url(r'^seminar$', SeminarListView.as_view(), name='seminar'),
    url(r'^event_report$', EventReportView.as_view(), name='event_report'),
    url(r'^write_post/?$', MakePostView.as_view(), name='write_post')
]