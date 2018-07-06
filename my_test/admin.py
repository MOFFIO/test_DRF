# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth import get_user_model
from my_test.models import User, Post, Like


admin_register = admin.site.register
admin_register(User)
admin_register(Post)
admin_register(Like)


class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'is_superuser']


class PostAdmin(admin.ModelAdmin):
    class Meta:
        model = get_user_model()
        fields = ['id', 'author', 'date_dump']

class LikeAdmin(admin.ModelAdmin):
    class Meta:
        model = get_user_model()
        fields = ['id', 'user', 'post','is_like']


