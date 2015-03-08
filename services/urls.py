from django.conf.urls import patterns, url, include

from tastypie.api import Api

from .api import ServiceResource
from .views import get_data, service_list

v1_api = Api(api_name='v1')
v1_api.register(ServiceResource())

urlpatterns = patterns(
    '',
    url(r'^pub/(?P<domain>[^/]+)/', get_data, name='get_data'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^list', service_list, name='service_list'),
)
