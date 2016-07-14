from board.models import Board, Post, Comment
from django.contrib import admin
from main.admin import admin_register

admin_register(Board, admin.ModelAdmin)
admin_register(Post, admin.ModelAdmin)
admin_register(Comment, admin.ModelAdmin)