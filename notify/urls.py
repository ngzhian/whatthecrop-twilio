from django.conf.urls import include, url
from django.contrib import admin

from .views import notify, console

urlpatterns = [
    url(r'^$', notify),
    url(r'^console/$', console),
]
