from django.conf.urls import include, url
from django.contrib import admin

from .views import handle_log

urlpatterns = [
    url(r'^$', handle_log),
]
