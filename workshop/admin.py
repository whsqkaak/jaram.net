from django.contrib import admin
from workshop.models import WorkShop, WorkShopTask, WorkShopTaskSubmission
from main.admin import admin_register

admin_register(WorkShop, admin.ModelAdmin)
admin_register(WorkShopTask, admin.ModelAdmin)
admin_register(WorkShopTaskSubmission, admin.ModelAdmin)
