from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from gallery.models import Album
from gallery.util.gphoto import GPhoto
from main.util import create_response


class GalleryView(TemplateView):
    template_name = 'gallery/list.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        response['albums'] = Album.objects.all()
        return render(request, self.template_name, response)


class GalleryDetailView(TemplateView):
    template_name = 'gallery/detail.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        response['album'] = Album.objects.get(pk=kwargs.get('id'))
        return render(request, self.template_name, response)


class GalleryLinkView(View):
    def get(self, request):
        data = request.GET
        gphoto = GPhoto.get()

        if data.get('code'):
            print('code', data.get('code'))
            gphoto.login(data.get('code'))
            print('login')
            gphoto.sync()
            print('sync')
        else:
            return redirect(gphoto.login())

        return redirect('gallery')