from board.models import Post, Board
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from main.util import create_response


class IntroView(TemplateView):
    template_name = 'intro.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class MainView(TemplateView):
    template_name = 'main.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)

        try:
            notice = Board.objects.get(name='공지사항')
            response['recent_posts'] = Post.objects.exclude(board=notice) \
                                      .filter(board__usable_group__in=request.user.groups.all()) \
                                      .order_by('-write_date')[:3]
            response['notice_posts'] = notice.post_set.order_by('-emphasis')[:3]
        except Board.DoesNotExist:
            notice = None

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
