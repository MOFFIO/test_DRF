# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import permissions, status, mixins
from rest_framework.authtoken.models import Token
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet



from my_test.models import Post
from my_test.serializers import PostSerializer, UserSerializer, MyAuthTokenSerializer, LikeSerializer, UnlikeSerializer


class AuthOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated


class PostView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthOrReadOnly,)
    http_method_names = ['get', 'post', 'put', 'head', 'option']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def like(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def unlike(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = UnlikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreateView(mixins.CreateModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    http_method_names = ['post']

    def token(self, request):
        serializer = MyAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        content = {
            'token': token.key
        }
        return Response(content)

    def signup(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('User created!', status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
