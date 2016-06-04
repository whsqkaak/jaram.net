from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from main.models import Member


def admin_register(model, user_admin):
    try:
        admin.site.register(model, user_admin)
    except AlreadyRegistered:
        admin.site.unregister(model)
        admin.site.register(model, user_admin)


admin_register(Member, admin.ModelAdmin)
