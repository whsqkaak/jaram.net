from board.views import PlayStormingView, EventReportView, SeminarListView, MakePostView, \
    PlayStormingListView, SeminarDetailView, PlayStormingDetailView, AnnouncementListView, GraduatingBoardListView, \
    StudentBoardListView, AnnouncementDetailView, GraduatingBoardDetailView, StudentBoardDetailView
from django.conf.urls import url

urlpatterns = [
    url(r'^playstorming$', PlayStormingListView.as_view(), name='playstorming'),
    url(r'^seminar$', SeminarListView.as_view(), name='seminar'),
    url(r'^seminar/(?P<id>\d+)/?$', SeminarDetailView.as_view(), name='seminar_detail'),
    url(r'^playstorming/(?P<id>\d+)/?$', PlayStormingDetailView.as_view(), name='playstorming_detail'),
    url(r'^event_report$', EventReportView.as_view(), name='event_report'),
    url(r'^write_post$', MakePostView.as_view(), name='write_post'),
    url(r'^announcement$', AnnouncementListView.as_view(), name='announcement'),
    url(r'^announcement/(?P<id>\d+)/?$', AnnouncementDetailView.as_view(), name='announcement_detail'),
    url(r'^graduating$', GraduatingBoardListView.as_view(), name='graduating'),
    url(r'^graduating/(?P<id>\d+)/?$', GraduatingBoardDetailView.as_view(), name='graduating_detail'),
    url(r'^student$', StudentBoardListView.as_view(), name='student'),
    url(r'^student/(?P<id>\d+)/?$', StudentBoardDetailView.as_view(), name='student_detail'),
]