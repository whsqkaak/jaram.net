from django.shortcuts import render, redirect
from django.views.generic import TemplateView


class GalleryView(TemplateView):
    template_name = ''

    def get(self, request, *args, **kwargs):
        return redirect('/main/?warning=준비중입니다.')