from django.shortcuts import render
from django.views.generic import TemplateView


class PlayStormingView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'board/postList.html', {})


class SeminarView(TemplateView):
    pass


class EventReportView(TemplateView):
    pass