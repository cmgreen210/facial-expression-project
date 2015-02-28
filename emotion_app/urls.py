from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

urlpatterns = patterns('',
    url(r'^emotion/', include('emotion.urls')),
    url(r'^$', RedirectView.as_view(url='/emotion/')),
)
