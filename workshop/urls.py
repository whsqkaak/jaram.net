from django.conf.urls import url
from workshop.views import WorkShopListView, WorkShopRegistrationView, WorkShopDetailView, WorkShopTaskListView,\
    WorkShopTaskSubmissionView, WorkShopTaskRegistrationView, \
    WorkShopTaskSubmissionListView, WorkShopTaskDetailView, \
    WorkShopTaskSubmissionDetailView, WorkShopTaskUpdateView, \
    WorkShopView

urlpatterns = [
    url(r'^ongoing/?$', WorkShopView.as_view(), name='workshop_ongoing'),
    url(r'^$', WorkShopListView.as_view(), name='workshop'),
    url(r'^registration/?$', WorkShopRegistrationView.as_view(), name='workshop_registration'),
    url(r'^(?P<id>\d+)/?$', WorkShopDetailView.as_view(), name='workshop_detail'),
    url(r'^taskList/?$', WorkShopTaskListView.as_view(), name='workshop_taskList'),
    url(r'^taskList/(?P<id>\d+)/?$', WorkShopTaskDetailView.as_view(), name='workshop_taskDetail'),
    url(r'^taskList/taskRegistration/?$', WorkShopTaskRegistrationView.as_view(), name='workshop_taskRegistration'),
    url(r'^taskList/(?P<id>\d+)/taskSubmission/?$', WorkShopTaskSubmissionView.as_view(), name='workshop_taskSubmission'),
    url(r'^taskList/(?P<id>\d+)/taskSubmissionList/?$',
        WorkShopTaskSubmissionListView.as_view(), name='workshop_taskSubmissionList'),
    url(r'^taskList/(?P<id>\d+)/taskSubmissionList/(?P<task_id>\d+)/?$',
        WorkShopTaskSubmissionDetailView.as_view(), name='workshop_taskSubmissionDetail'),
    url(r'^taskList/(?P<id>\d+)/taskUpdate/(?P<task_id>\d+)/?$', WorkShopTaskUpdateView.as_view(), name='workshop_taskUpdate'),
]