from django.conf.urls import url
import django.contrib.auth.views
from main.views import IntroView, MainView, ProfileView, SignUpView, SitemapView, TermsAndConditionsView

urlpatterns = [
    url(r'^$|^intro', IntroView.as_view(), name='intro'),
    url(r'^login', django.contrib.auth.views.login, name='login', kwargs={'template_name': 'login.html'}),
    url(r'^logout', django.contrib.auth.views.logout, name='logout', kwargs={'next_page': '/'}),
    url(r'^main', MainView.as_view(), name='homepage_main'),
    url(r'^profile', ProfileView.as_view(), name='profile'),
    url(r'^sign_up', SignUpView.as_view(), name='sign_up'),
    url(r'^sitemap', SitemapView.as_view(), name='sitemap'),
    url(r'^termsAndConditions', TermsAndConditionsView.as_view(), name='terms_and_conditions')
]
