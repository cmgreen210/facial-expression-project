from django.conf.urls import url, patterns
import emotion.views

urlpatterns = patterns('',
    url(r'^$', emotion.views.get_video, name='video'),
)
