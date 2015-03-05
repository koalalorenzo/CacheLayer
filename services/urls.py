from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns(
    '',
    url(r'^pub/(?P<domain>[^/]+)/', get_data, name='get_data'),
)
