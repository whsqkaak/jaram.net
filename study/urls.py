from django.conf.urls import url
from study.views import StudyListView, StudyDetailView, StudyReportView

urlpatterns = [
    url(r'^$', StudyListView.as_view(), name='study'),
    url(r'^(?P<id>\d+)/?$', StudyDetailView.as_view(), name='study_detail'),
    url(r'^(?P<id>\d+)/report/?$', StudyReportView.as_view(), name='study_report'),
]