from django.conf.urls import url

from main.views import IntroView, MainView, ProfileView, SignUpView, SitemapView


urlpatterns = [
    url(r'^$|^intro', IntroView.as_view(), name='intro'),
    url(r'^login', 'django.contrib.auth.views.login', name='login', kwargs={'template_name': 'login.html'}),
    url(r'^logout', 'django.contrib.auth.views.logout', name='logout', kwargs={'next_page': '/'}),
    url(r'^main', MainView.as_view(), name='homepage_main'),
]