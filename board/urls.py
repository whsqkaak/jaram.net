from board.views import PlayStormingView, EventReportView, SeminarListView, MakePostView, \
    PlayStormingListView, SeminarDetailView, PlayStormingDetailView
from django.conf.urls import url

urlpatterns = [
    url(r'^playstorming$', PlayStormingListView.as_view(), name='playstorming'),
    url(r'^seminar$', SeminarListView.as_view(), name='seminar'),
    url(r'^seminar/(?P<id>\d+)/?$', SeminarDetailView.as_view(), name='seminar_detail'),
    url(r'^playstorming/(?P<id>\d+)/?$', PlayStormingDetailView.as_view(), name='playstorming_detail'),
    url(r'^event_report$', EventReportView.as_view(), name='event_report'),
    url(r'^write_post$', MakePostView.as_view(), name='write_post')
]