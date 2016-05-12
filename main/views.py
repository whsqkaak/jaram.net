from django.shortcuts import render
from django.views.generic import TemplateView


class MainView(TemplateView):
    template_name = 'main.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class LoginView(TemplateView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)