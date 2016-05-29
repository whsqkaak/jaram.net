from django.shortcuts import render
from django.views.generic import TemplateView
from main.util import create_response
from study.models import Study


class StudyListView(TemplateView):
    template_name = 'list.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        response['page'] = Study.objects.filter(is_active=True).all()
        return render(request, self.template_name, response)