from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from main.util import create_response
from board.models import Seminar, PlayStorming, Announcement, GraduatingBoard, \
    StudentBoard
from itertools import chain
from operator import attrgetter

class IntroView(TemplateView):
    template_name = 'intro.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class MainView(TemplateView):
    template_name = 'main.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)

        new_page = []
        new_page = chain(new_page, (Seminar.objects.order_by('-write_date').all()))
        new_page = chain(new_page, (PlayStorming.objects.order_by('-write_date').all()))
        new_page = chain(new_page, (GraduatingBoard.objects.order_by('-write_date').all()))
        new_page = chain(new_page, (StudentBoard.objects.order_by('-write_date').all()))
        new_page = sorted(new_page, key=attrgetter('write_date'), reverse=True)
        response['new_page'] = new_page[:3]

        if(len(new_page) >= 1):
            response['dir_0'] = new_page[0].__class__.__name__
        if(len(new_page) >= 2):
            response['dir_1'] = new_page[1].__class__.__name__
        if(len(new_page) >= 3):
            response['dir_2'] = new_page[2].__class__.__name__

        announce_page = Announcement.objects.all()
        announce_page_important = Announcement.objects.filter(importance=True).all()
        response['announce_page'] = (list(announce_page_important) + list(announce_page))[:3]

        return render(request, self.template_name, response)


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        return render(request, self.template_name, response)

    def post(self, request, *args, **kwargs):
        data = request.POST
        if not data.get('email'):
            return redirect('/profile?error=이메일을 입력해주세요')

        user = request.user

        user.email = data.get('email')
        user.phone = data.get('phone', '')
        user.sns = data.get('sns', '')
        user.save()

        return redirect('profile')
