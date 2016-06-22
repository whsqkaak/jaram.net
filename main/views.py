from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from main.util import create_response


class IntroView(TemplateView):
    template_name = 'intro.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class MainView(TemplateView):
    template_name = 'main.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        return render(request, self.template_name, response)


class SeminarView(TemplateView):
    template_name = 'postList.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        return render(request, self.template_name, response)
