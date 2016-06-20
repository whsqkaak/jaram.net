from django.conf.urls import url

from main.views import IntroView, LoginView, MainView, LogoutView, SeminarView

urlpatterns = [
    url(r'^$|^intro', IntroView.as_view(), name='intro'),
    url(r'^login', LoginView.as_view(), name='login'),
    url(r'^logout', LogoutView.as_view(), name='logout'),
    url(r'^main', MainView.as_view(), name='homepage_main'),
    url(r'^seminar', SeminarView.as_view(), name='seminar'),
]