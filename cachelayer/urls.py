from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^', include('services.urls')),
    url(r'^robots.txt$', 'cachelayer.views.robots'),
    url(r'^admin/', include(admin.site.urls)),
)

# Servering static files too
urlpatterns += patterns(
    'django.contrib.staticfiles.views',
    url(r'^static/(?P<path>.*)$', 'serve'),
)
