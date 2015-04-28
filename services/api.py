from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie import fields

from .models import Service


class ServiceResource(ModelResource):
    is_down = fields.BooleanField(attribute='is_down', readonly=True)
    endpoint = fields.CharField(attribute='endpoint', readonly=True)

    class Meta:
        queryset = Service.objects.all().order_by("-edited_at")
        resource_name = 'service'
        allowed_methods = ['get', 'post', 'put', 'delete']
        excludes = [
            'force_down', 'is_crawler_enabled', 'is_enabled',
            'created_at', 'edited_at', 'crawled_at',
        ]
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True
