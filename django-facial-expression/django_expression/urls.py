from django.conf.urls import url, patterns

from expression.views import *


urlpatterns = patterns('',
                       url(r'^$', home_page, name='home'),
                       url(r'^image/$', UploadImageFromURLView.as_view(),
                           name='image'),
                       url(r'^example/(?P<ex_name>\w+)', example_view)
                       )
