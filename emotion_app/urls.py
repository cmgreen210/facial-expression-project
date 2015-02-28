from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^emotion/', include('emotion.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
