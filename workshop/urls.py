from django.conf.urls import url
from workshop.views import WorkshopView

urlpatterns = [
    url(r'^$', WorkshopView.as_view(), name='workshop'),
]