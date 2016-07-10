from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from main.util import create_response
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from board.models import Seminar, PlayStorming, SeminarComment, PlayStormingComment
from main.utils.paginator import easy_paginator


class SeminarListView(TemplateView):
    template_name = 'postList.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)

        easy_paginator(Seminar.objects.all(), request.GET.get('page', 1), each_data_count=6, display_button_range=3,
                       save_to=response)

        response['header_title'] = '세미나'
        response['dir'] = 'seminar'
        return render(request, self.template_name, response)


class MakePostView(TemplateView):
    template_name = 'makePost.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        response['header_title'] = '게시글 작성'
        response['target'] = request.GET.get('type')
        if not response['target']:
            pass

        return render(request, self.template_name, response)

    def post(self, request, *args, **kwargs):
        data = request.POST
        type = data.get('post_type')

        if type == 'seminar':
            model = Seminar
        elif type == 'playstorming':
            model = PlayStorming

        model(writer=request.user,
              write_date=timezone.now(),
              title=data.get('title'),
              content=data.get('content'),
              attachment=request.FILES.get('attachment')).save()

        return redirect('/board/' + type + '?success=성공적으로 등록되었습니다.')


class PlayStormingListView(TemplateView):
    template_name = 'postList.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        easy_paginator(PlayStorming.objects.all(), request.GET.get('page', 1), each_data_count=6,
                       display_button_range=3,
                       save_to=response)
        response['dir'] = 'playstorming'
        response['header_title'] = '플레이스토밍'
        return render(request, self.template_name, response)


class PlayStormingView(TemplateView):
    template_name = 'postList.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)

        response['header_title'] = '플레이스토밍'
        return render(request, self.template_name, response)


class SeminarDetailView(TemplateView):
    template_name = 'board_detail.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)

        try:
            seminar = Seminar.objects.get(pk=kwargs.get('id'))
        except ObjectDoesNotExist:
            return redirect('/seminar?error=존재하지 않는 게시글입니다.')

        response['seminar'] = seminar
        response['header_title'] = '세미나'
        response['comments'] = seminar.seminarcomment_set.order_by('-write_date').all()
        return render(request, self.template_name, response)

    def post(self, request, *args, **kwargs):
        data = request.POST
        try:
            seminar = Seminar.objects.get(pk=kwargs.get('id'))
        except ObjectDoesNotExist:
            return redirect('/board/seminar?error=존재하지 않는 게시글입니다.')

        if not (data.get('content')):
            return redirect('/board/seminar?error=입력된 정보가 올바르지 않습니다.')

        SeminarComment(writer=request.user,
                       board=seminar,
                       write_date=timezone.now(),
                       content=data.get('content')).save()

        return redirect('/board/seminar/' + kwargs.get('id') + '?success=성공적으로 등록되었습니다.')


class PlayStormingDetailView(TemplateView):
    template_name = 'board_detail.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)

        try:
            playstorming = PlayStorming.objects.get(pk=kwargs.get('id'))
        except ObjectDoesNotExist:
            return redirect('/playstorming?error=존재하지 않는 게시글입니다.')

        response['seminar'] = playstorming
        response['header_title'] = '세미나'
        response['comments'] = playstorming.playstormingcomment_set.order_by('-write_date').all()
        return render(request, self.template_name, response)

    def post(self, request, *args, **kwargs):
        data = request.POST
        try:
            seminar = PlayStorming.objects.get(pk=kwargs.get('id'))
        except ObjectDoesNotExist:
            return redirect('/board/playstorming?error=존재하지 않는 게시글입니다.')

        if not (data.get('content')):
            return redirect('/board/playstorming?error=입력된 정보가 올바르지 않습니다.')

        PlayStormingComment(writer=request.user,
                            board=seminar,
                            write_date=timezone.now(),
                            content=data.get('content')).save()

        return redirect('/board/playstorming/' + kwargs.get('id') + '?success=성공적으로 등록되었습니다.')


class EventReportView(TemplateView):
    template_name = 'eventList.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        response['header_title'] = '일정'
        return render(request, self.template_name, response)
