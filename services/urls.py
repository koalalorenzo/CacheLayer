from django.conf.urls import patterns, url

from .views import get_data, service_list

urlpatterns = patterns(
    '',
    url(r'^pub/(?P<domain>[^/]+)/', get_data, name='get_data'),
)
