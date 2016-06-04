from django.contrib import admin
from main.admin import admin_register
from study.models import Study


admin_register(Study, admin.ModelAdmin)