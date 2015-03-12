from django.conf.urls import url, patterns
from emotion.views import *


urlpatterns = patterns('',
                       url(r'^$', home_page, name='home'),
                       # url(r'^video/$', emotion.views.get_video, name='video'),
                       url(r'^image/$', UploadImageFromURLView.as_view(),
                           name='image'),
                       )
