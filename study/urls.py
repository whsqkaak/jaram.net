from django.conf.urls import url
from study.views import StudyListView, StudyDetailView, StudyReportView, StudyRegistrationView, SearchUserApiView

urlpatterns = [
    url(r'^$', StudyListView.as_view(), name='study'),
    url(r'^registration/?$', StudyRegistrationView.as_view(), name='study_registration'),
    url(r'^(?P<id>\d+)/?$', StudyDetailView.as_view(), name='study_detail'),
    url(r'^(?P<id>\d+)/report/?$', StudyReportView.as_view(), name='study_report'),
    url(r'^api/search_user/?$', SearchUserApiView.as_view(), name='study_api_search_user'),
]