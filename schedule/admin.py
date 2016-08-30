from django.contrib import admin
from main.admin import admin_register
from schedule.models import Event

admin_register(Event, admin.ModelAdmin)
