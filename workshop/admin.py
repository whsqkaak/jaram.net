from django.contrib import admin
from main.admin import admin_register
from workshop.models import WorkShop


admin_register(WorkShop, admin.ModelAdmin)
# Register your models here.
