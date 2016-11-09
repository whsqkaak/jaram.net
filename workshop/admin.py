from django.contrib import admin
from workshop.models import WorkShop
from main.admin import admin_register

admin_register(WorkShop, admin.ModelAdmin)