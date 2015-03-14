from django.conf.urls import patterns, include, url
from django.contrib import admin

from tastypie.api import Api

from services.api import ServiceResource
# from .api import UserResource

v1_api = Api(api_name='v1')
v1_api.register(ServiceResource())
# v1_api.register(UserResource())

urlpatterns = patterns(
    '',
    url(r'^', include('services.urls')),
    url(r'^robots.txt$', 'cachelayer.views.robots'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^admin/', include(admin.site.urls)),
)

# Servering static files too
urlpatterns += patterns(
    'django.contrib.staticfiles.views',
    url(r'^static/(?P<path>.*)$', 'serve'),
)
