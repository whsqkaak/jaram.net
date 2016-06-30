import json
from datetime import datetime

import httplib2
import os
import xmltodict
from dateutil import parser
from dateutil.tz import gettz
from django.conf import settings
from gallery.models import Album, Photo
from oauth2client.client import OAuth2WebServerFlow


class GPhoto:
    _instance = None

    credentials = None
    flow = None

    exclude_album = [1000000462352115]

    @staticmethod
    def get():
        if not GPhoto._instance:
            GPhoto._instance = GPhoto()

        return GPhoto._instance

    def login(self, code=None):
        if code and self.flow:
            self.credentials = self.flow.step2_exchange(code)
            return self.credentials

        self.flow = OAuth2WebServerFlow(
            client_id='421894677908-5qnbquo0l9ct5l7lrqfd6slkaklvd25i.apps.googleusercontent.com',
            client_secret='uj3wCTPUgQ6SdZ6C3_xmFnUp',
            scope='https://picasaweb.google.com/data/',
            redirect_uri=settings.URL + '/gallery/link'
        )

        return self.flow.step1_get_authorize_url()

    def is_logged(self):
        return self.credentials is not None

    def request(self, url, method='GET', body=''):
        http = httplib2.Http()
        http = self.credentials.authorize(http)
        response, content = http.request(
            uri='https://picasaweb.google.com/data' + url,
            method=method,
            headers={'GData-Version': 2, 'charset': 'UTF-8'},
            body=body
        )
        return content

    def get_album(self):
        result = []
        response = xmltodict.parse(self.request('/feed/api/user/default'))
        if not response:
            return result

        albums = response['feed'].get('entry')

        if not albums:
            return result

        for album in albums:
            if int(album['gphoto:id']) in GPhoto.exclude_album:
                continue

            result.append(dict(
                id=album['gphoto:id'],
                title=album['title'],
                description=album['media:group']['media:description'].get('#text', ''),
                main_url=album['media:group']['media:content'].get('@url', ''),
                thumbnail_url=album['media:group']['media:thumbnail'].get('@url', ''),
                date=datetime.fromtimestamp(int(album['gphoto:timestamp']) / 1000),
                pub_date=parser.parse(album['published']),
                update_date=parser.parse(album['updated']),
            ))

        return result

    def get_photo(self, gphoto_album_id):
        result = []
        response = xmltodict.parse(self.request('/feed/api/user/default/albumid/' + str(gphoto_album_id)))
        if not response:
            return result

        photos = response['feed'].get('entry')

        if not photos:
            return result

        for photo in photos:
            image_url = photo['content']['@src']
            image_url_split = str(image_url).rsplit('/', 1)

            result.append(dict(
                id=photo['gphoto:id'],
                album_id=photo['gphoto:albumid'],
                title=photo['title'],
                description=photo['media:group']['media:description'].get('#text', ''),
                image_url=image_url,
                image_2048_url=image_url_split[0] + '/s2048/' + image_url_split[1],
                image_origin_url=image_url_split[0] + '/s16383/' + image_url_split[1],
                date=datetime.fromtimestamp(int(photo['gphoto:timestamp']) / 1000, tz=gettz(settings.TIME_ZONE)),
                pub_date=parser.parse(photo['published']),
                update_date=parser.parse(photo['updated']),
            ))

        return result

    def _sync_album(self):
        albums = self.get_album()
        Album.objects.all().delete()
        for album in albums:
            album_obj = Album()
            album_obj.gphoto_id = album['id']
            album_obj.title = album['title']
            album_obj.description = album['description']
            album_obj.main_url = album['main_url']
            album_obj.thumbnail_url = album['thumbnail_url']
            album_obj.date = album['date']
            album_obj.pub_date = album['pub_date']
            album_obj.update_date = album['update_date']
            album_obj.save()

    def _sync_photo(self):
        for album in Album.objects.all():
            for photo in self.get_photo(album.gphoto_id):
                photo_obj = Photo()
                photo_obj.album = album
                photo_obj.gphoto_id = photo['id']
                photo_obj.title = photo['title']
                photo_obj.description = photo['description']
                photo_obj.image_url = photo['image_url']
                photo_obj.image_2048_url = photo['image_2048_url']
                photo_obj.image_origin_url = photo['image_origin_url']
                photo_obj.date = photo['date']
                photo_obj.pub_date = photo['pub_date']
                photo_obj.update_date = photo['update_date']
                photo_obj.save()

    def sync(self):
        self._sync_album()
        self._sync_photo()
