from django.utils import timezone
from main.util import create_response
from django.shortcuts import render
from django.views.generic import TemplateView
from board.models import Seminar
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class SeminarListView(TemplateView):
    template_name = 'postList.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        page = request.GET.get('page', 1)
        post_list = Seminar.objects.all()
        paginator = Paginator(post_list, 10)

        try:
            response['posts'] = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            response['posts'] = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            response['posts'] = paginator.page(paginator.num_pages)
        response['header_title'] = '세미나'
        return render(request, self.template_name, response)


class MakePostView(TemplateView):
    template_name = 'makePost.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        response['header_title'] = '게시글 작성'
        return render(request, self.template_name, response)

    def post(self, request, *args, **kwargs):
        data = request.POST
        Seminar(writer=request.user,
                write_date=timezone.now(),
                title=data.get('title'),
                content=data.get('content'),
                attachment=data.FILES.get('attachment')).save()


class PlayStormingView(TemplateView):
    template_name = 'postList.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        response['header_title'] = '플레이스토밍'
        return render(request, self.template_name, response)


class SeminarView(TemplateView):
    template_name = 'postList.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        response['posts'] = Seminar.objects.all()
        response['header_title'] = '세미나'
        return render(request, self.template_name, response)


class EventReportView(TemplateView):
    template_name = 'eventList.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        response['header_title'] = '일정'
        return render(request, self.template_name, response)
