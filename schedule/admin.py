from django.contrib import admin
from main.admin import admin_register
from schedule.models import Event, EventGroup

admin_register(Event, admin.ModelAdmin)
admin_register(EventGroup, admin.ModelAdmin)