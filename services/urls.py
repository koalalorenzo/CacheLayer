from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns(
    '',
    url(r'^(?P<service_reference>\d+)', get_data, name='get_data'),
)
