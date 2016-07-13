from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from main.util import create_response
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from board.models import Seminar, PlayStorming, SeminarComment, PlayStormingComment, Announcement, GraduatingBoard, \
    StudentBoard, GraduatingBoardComment, StudentBoardComment
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
        response['header_title'] = '게시글 수정'
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
        elif type == 'announcement':
            model = Announcement
        elif type == 'graduating':
            model = GraduatingBoard
        elif type == 'student':
            model = StudentBoard

        print(request.FILES.get('attachment'))

        model(writer=request.user,
              write_date=timezone.now(),
              title=data.get('title'),
              content=data.get('content'),
              attachment=request.FILES.get('attachment')).save()

        return redirect('/board/' + type + '?success=성공적으로 등록되었습니다.')


class EditPostView(TemplateView):
    template_name = 'editPost.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        response['header_title'] = '게시글 수정'
        response['target'] = request.GET.get('type')
        if not response['target']:
            pass
        type = request.GET.get('type')

        if type == 'seminar':
            model = Seminar
        elif type == 'playstorming':
            model = PlayStorming
        elif type == 'announcement':
            model = Announcement
        elif type == 'graduating':
            model = GraduatingBoard
        elif type == 'student':
            model = StudentBoard
        post = model.objects.get(pk=request.GET.get('id'))
        response['post'] = post
        return render(request, self.template_name, response)

    def post(self, request, *args, **kwargs):
        data = request.POST
        type = data.get('post_type')

        if type == 'seminar':
            model = Seminar
        elif type == 'playstorming':
            model = PlayStorming
        elif type == 'announcement':
            model = Announcement
        elif type == 'graduating':
            model = GraduatingBoard
        elif type == 'student':
            model = StudentBoard

        post = model.objects.get(pk=request.GET.get('id'))

        post.title = data.get('title')
        post.content = data.get('content')
        post.attachment=request.FILES.get('attachment')

        post.save()

        return redirect('/board/' + type + '/' + request.GET.get('id') + '?success=성공적으로 수정되었습니다.')


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

        response['post'] = seminar
        response['dir'] = 'seminar'
        response['header_title'] = '세미나'
        response['comments'] = seminar.seminarcomment_set.order_by('-write_date').all()
        return render(request, self.template_name, response)

    def post(self, request, *args, **kwargs):
        data = request.POST
        try:
            post = Seminar.objects.get(pk=kwargs.get('id'))
        except ObjectDoesNotExist:
            return redirect('/board/seminar?error=존재하지 않는 게시글입니다.')

        if not (data.get('content')):
            return redirect('/board/seminar?error=입력된 정보가 올바르지 않습니다.')
        SeminarComment(writer=request.user,
                       board=post,
                       write_date=timezone.now(),
                       content=data.get('content')).save()

        return redirect('/board/seminar/' + kwargs.get('id') + '?success=성공적으로 등록되었습니다.')


class SeminarDeleteView(TemplateView):
    template_name = 'board_detail.html'

    def get(self, request, *args, **kwargs):
        seminar = Seminar.objects.get(pk=kwargs.get('id'))
        seminar.delete()

        return redirect('/board/seminar?success=삭제되었습니다.')


class PlayStormingDeleteView(TemplateView):
    template_name = 'board_detail.html'

    def get(self, request, *args, **kwargs):
        playstorming = PlayStorming.objects.get(pk=kwargs.get('id'))
        playstorming.delete()

        return redirect('/board/playstorming?success=삭제되었습니다.')


class PlayStormingDetailView(TemplateView):
    template_name = 'board_detail.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)

        try:
            playstorming = PlayStorming.objects.get(pk=kwargs.get('id'))
        except ObjectDoesNotExist:
            return redirect('/playstorming?error=존재하지 않는 게시글입니다.')

        response['post'] = playstorming
        response['dir'] = 'playstorming'
        response['header_title'] = '플레이스토밍'
        response['comments'] = playstorming.playstormingcomment_set.order_by('-write_date').all()
        return render(request, self.template_name, response)

    def post(self, request, *args, **kwargs):
        data = request.POST
        try:
            post = PlayStorming.objects.get(pk=kwargs.get('id'))
        except ObjectDoesNotExist:
            return redirect('/board/playstorming?error=존재하지 않는 게시글입니다.')

        if not (data.get('content')):
            return redirect('/board/playstorming?error=입력된 정보가 올바르지 않습니다.')

        PlayStormingComment(writer=request.user,
                            board=post,
                            write_date=timezone.now(),
                            content=data.get('content')).save()

        return redirect('/board/playstorming/' + kwargs.get('id') + '?success=성공적으로 등록되었습니다.')


class EventReportView(TemplateView):
    template_name = 'eventList.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        response['header_title'] = '일정'
        return render(request, self.template_name, response)


class AnnouncementListView(TemplateView):
    template_name = 'postList.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        easy_paginator(Announcement.objects.all(), request.GET.get('page', 1), each_data_count=6,
                       display_button_range=3,
                       save_to=response)
        response['dir'] = 'announcement'
        response['header_title'] = '공지사항'
        return render(request, self.template_name, response)


class AnnouncementDetailView(TemplateView):
    template_name = 'board_detail.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)

        try:
            announcement = Announcement.objects.get(pk=kwargs.get('id'))
        except ObjectDoesNotExist:
            return redirect('/announcement?error=존재하지 않는 게시글입니다.')

        response['post'] = announcement
        response['dir'] = 'announcement'
        response['header_title'] = '공지사항'
        return render(request, self.template_name, response)


class AnnouncementDeleteView(TemplateView):
    template_name = 'board_detail.html'

    def get(self, request, *args, **kwargs):
        announcement = Announcement.objects.get(pk=kwargs.get('id'))
        announcement.delete()

        return redirect('/board/announcement?success=삭제되었습니다.')


class GraduatingBoardListView(TemplateView):
    template_name = 'postList.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        easy_paginator(GraduatingBoard.objects.all(), request.GET.get('page', 1), each_data_count=6,
                       display_button_range=3,
                       save_to=response)
        response['dir'] = 'graduating'
        response['header_title'] = '졸업생게시판'
        return render(request, self.template_name, response)


class GraduatingBoardDetailView(TemplateView):
    template_name = 'board_detail.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)

        try:
            graduating = GraduatingBoard.objects.get(pk=kwargs.get('id'))
        except ObjectDoesNotExist:
            return redirect('/graduating?error=존재하지 않는 게시글입니다.')

        response['post'] = graduating
        response['dir'] = 'graduating'
        response['header_title'] = '졸업생게시판'
        response['comments'] = graduating.graduatingboardcomment_set.order_by('-write_date').all()
        return render(request, self.template_name, response)

    def post(self, request, *args, **kwargs):
        data = request.POST
        try:
            post = GraduatingBoard.objects.get(pk=kwargs.get('id'))
        except ObjectDoesNotExist:
            return redirect('/board/graduating?error=존재하지 않는 게시글입니다.')

        if not (data.get('content')):
            return redirect('/board/graduating?error=입력된 정보가 올바르지 않습니다.')

        GraduatingBoardComment(writer=request.user,
                               board=post,
                               write_date=timezone.now(),
                               content=data.get('content')).save()

        return redirect('/board/graduating/' + kwargs.get('id') + '?success=성공적으로 등록되었습니다.')


class GraduatingBoardDeleteView(TemplateView):
    template_name = 'board_detail.html'

    def get(self, request, *args, **kwargs):
        graduating = GraduatingBoard.objects.get(pk=kwargs.get('id'))
        graduating.delete()

        return redirect('/board/graduating?success=삭제되었습니다.')


class StudentBoardListView(TemplateView):
    template_name = 'postList.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        easy_paginator(StudentBoard.objects.all(), request.GET.get('page', 1), each_data_count=6,
                       display_button_range=3,
                       save_to=response)
        response['dir'] = 'student'
        response['header_title'] = '재학생게시판'
        return render(request, self.template_name, response)


class StudentBoardDetailView(TemplateView):
    template_name = 'board_detail.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)

        try:
            student = StudentBoard.objects.get(pk=kwargs.get('id'))
        except ObjectDoesNotExist:
            return redirect('/graduating?error=존재하지 않는 게시글입니다.')

        response['post'] = student
        response['dir'] = 'student'
        response['header_title'] = '재학생게시판'
        response['comments'] = student.studentboardcomment_set.order_by('-write_date').all()
        return render(request, self.template_name, response)

    def post(self, request, *args, **kwargs):
        data = request.POST
        try:
            post = StudentBoard.objects.get(pk=kwargs.get('id'))
        except ObjectDoesNotExist:
            return redirect('/board/student?error=존재하지 않는 게시글입니다.')

        if not (data.get('content')):
            return redirect('/board/student?error=입력된 정보가 올바르지 않습니다.')

        StudentBoardComment(writer=request.user,
                            board=post,
                            write_date=timezone.now(),
                            content=data.get('content')).save()

        return redirect('/board/student/' + kwargs.get('id') + '?success=성공적으로 등록되었습니다.')


class StudentBoardDeleteView(TemplateView):
    template_name = 'board_detail.html'

    def get(self, request, *args, **kwargs):
        student = StudentBoard.objects.get(pk=kwargs.get('id'))
        student.delete()

        return redirect('/board/student?success=삭제되었습니다.')