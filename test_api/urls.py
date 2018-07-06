# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin

from my_test import views

urlpatterns = [
    url(r'^post', views.PostView.as_view({'get': 'list', 'post': 'create'})),
    url(r'^post/(?P<pk>([0-9a-zA-Z])+)/like$', views.PostView.as_view({'put': 'like'})),
    url(r'^post/(?P<pk>([0-9a-zA-Z])+)/unlike$', views.PostView.as_view({'put': 'unlike'})),
    url(r'^user/signup/', views.UserCreateView.as_view({'post': 'signup'})),
    url(r'^user/token/', views.UserCreateView.as_view({'post': 'token'})),
    url(r'^admin/', admin.site.urls),

]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]