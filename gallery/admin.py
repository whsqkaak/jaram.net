from django.contrib import admin
from gallery.models import Album, Photo
from main.admin import admin_register

admin_register(Album, admin.ModelAdmin)
admin_register(Photo, admin.ModelAdmin)
