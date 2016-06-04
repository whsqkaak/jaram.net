from django.contrib import admin
from main.admin import admin_register
from study.models import Study, StudyReport

admin_register(Study, admin.ModelAdmin)
admin_register(StudyReport, admin.ModelAdmin)