# -*- coding: utf-8 -*-
"""lfora URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin', include(admin.site.urls)),
    url(r'^api/verify', include('verify.urls', namespace='verify')),
    url(r'^api/user', include('user_.urls', namespace='user')),
    url(r'^api/auth', include('auth_.urls', namespace='auth')),
    url(r'^api/oss', include('oss.urls', namespace='oss')),
    url(r'^api/work_order', include('workorder.urls', namespace='work_order')),
    url(r'^api/curriculum', include('curriculum.urls', namespace='curriculum')),
    url(r'^api/video', include('curriculum.video.urls', namespace='video')),
    url(r'^api/vod', include('vod.urls', namespace='vod')),

]
