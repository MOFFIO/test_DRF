# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, BaseUserManager
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save


def get_id():
    return str(uuid.uuid4()).replace('-', '')[:10]

class MyUserManager(BaseUserManager):

    def create_user(self, email, password, **more_fields):
        if not email:
            raise ValueError('No email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **more_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **more_fields):
        more_fields.setdefault('is_staff', True)
        more_fields.setdefault('is_superuser', True)
        more_fields.setdefault('is_active', True)

        if more_fields.get('is_staff') is not True:
            raise ValueError('oops')
        if more_fields.get('is_superuser') is not True:
            raise ValueError('oops')
        return self._create_user(email, password, **more_fields)


class BaseModel(models.Model):
    id = models.CharField(primary_key=True, default=get_id, editable=False, max_length=30, unique=True)
    date_dump = models.DateTimeField(editable=False, auto_now_add=True)
    date_updated = models.DateTimeField(editable=False, auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(_('email'), unique=True)
    objects = MyUserManager()
    is_staff = models.BooleanField(_('staff status'), default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Post(BaseModel):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.PROTECT)


class Like(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    is_like = models.BooleanField(default=True)
