from django.conf.urls import url, patterns
import emotion.views


urlpatterns = patterns('',
                       url(r'^$', emotion.views.home_page, name='home'),
                       url(r'^video/$', emotion.views.get_video, name='video'),
                       url(r'^image/$', emotion.views.get_image, name='image'),
                       )
