from django.conf.urls import url
from gallery.views import GalleryView, GalleryLinkView, GalleryDetailView

urlpatterns = [
    url(r'^$', GalleryView.as_view(), name='gallery'),
    url(r'^(?P<id>\d+)/?$', GalleryDetailView.as_view(), name='gallery_detail'),
    url(r'^link$', GalleryLinkView.as_view(), name='gallery_link'),
]
