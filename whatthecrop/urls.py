from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^l/', include('rawlog.urls')),
    url(r'^n/', include('notify.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
