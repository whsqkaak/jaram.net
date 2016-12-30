from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from gallery.models import Album
from gallery.util.gphoto import GPhoto
from main.util import create_response
from main.models import Grade


class GalleryView(TemplateView):
    template_name = 'gallery/list.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        if request.user.grade == Grade.objects.get(name='미승인'):
            return redirect('/main?warning=권한이 없습니다.')
        response['albums'] = Album.objects.all()
        return render(request, self.template_name, response)


class GalleryDetailView(TemplateView):
    template_name = 'gallery/detail.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        if request.user.grade == Grade.objects.get(name='미승인'):
            return redirect('/main?warning=권한이 없습니다.')
        response['album'] = Album.objects.get(pk=kwargs.get('id'))
        return render(request, self.template_name, response)


class GalleryLinkView(View):
    def get(self, request):
        data = request.GET
        gphoto = GPhoto.get()
        if request.user.grade == Grade.objects.get(name='미승인'):
            return redirect('/main?warning=권한이 없습니다.')
        if data.get('code'):
            gphoto.login(data.get('code'))
            gphoto.sync()
        else:
            return redirect(gphoto.login())

        return redirect('gallery')