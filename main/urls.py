from django.conf.urls import url

from main.views import MainView, LoginView

urlpatterns = [
    url(r'^$', MainView.as_view(), name='homepage_main'),
    url(r'^login$', LoginView.as_view(), name='login'),
]