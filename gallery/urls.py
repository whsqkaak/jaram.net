from django.conf.urls import url

from main.views import MainView

urlpatterns = [
    url(r'^$', MainView.as_view(), name='homepage_main'),
]