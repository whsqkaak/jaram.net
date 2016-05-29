from django.conf.urls import url
from study.views import StudyListView

urlpatterns = [
    url(r'^$', StudyListView.as_view(), name='study'),
]