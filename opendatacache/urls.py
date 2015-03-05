from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^', include('services.urls')),
    url(r'^robots.txt$', 'opendatacache.views.robots'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.contrib.staticfiles.views',
	url(r'^static/(?P<path>.*)$', 'serve'),
)