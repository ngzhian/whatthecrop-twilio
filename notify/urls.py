from django.conf.urls import include, url
from django.contrib import admin

from .views import notify

urlpatterns = [
    url(r'^$', notify),
]
