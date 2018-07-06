# -*- coding: utf-8 -*-

from django.utils.translation import gettext as _
from django.contrib.auth import authenticate
from django.core import exceptions
from rest_framework import serializers

from my_test.models import User, Post, Like


class MyAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attributes):
        email_or_username = attributes.get('email')
        password = attributes.get('password')

        if email_or_username and password:
            user = authenticate(email=email_or_username, password=password)
            if user:
                if not user.is_active:
                    info = _('User is not active')
                    raise exceptions.ValidationError(info)
            else:
                info = _('Unable login')
                raise exceptions.ValidationError(info)
        else:
            info = _('Input email and password')
            raise exceptions.ValidationError(info)

        attributes['user'] = user
        return attributes


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'content', 'date_dump')

class LikeSerializer(serializers.ModelSerializer):
    is_like = serializers.BooleanField(read_only=True)
    post = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'is_like', 'post', 'user')

    def create(self, validated_data):
        instance = Like.objects.update_or_create(validated_data, defaults={'is_like': True})
        return instance


class UnlikeSerializer(serializers.ModelSerializer):
    is_like = serializers.BooleanField(read_only=True)
    post = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'is_like', 'post', 'user')

    def create(self, validated_data):
        instance = Like.objects.update_or_create(validated_data, defaults={'is_like': False})
        return instance
