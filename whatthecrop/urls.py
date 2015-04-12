from django.conf.urls import include, url
from django.contrib import admin

from rawlog.views import FarmDataList, RawLogList

urlpatterns = [
    url(r'^l/', include('rawlog.urls')),
    url(r'^n/', include('notify.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rawlog/$', RawLogList.as_view()),
    url(r'^farmdata/$', FarmDataList.as_view()),
]
