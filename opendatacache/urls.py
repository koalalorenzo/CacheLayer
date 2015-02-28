from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'opendatacache.views.home', name='home'),
    url(r'^', include('services.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
