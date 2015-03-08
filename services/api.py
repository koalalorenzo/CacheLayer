from tastypie.resources import ModelResource
from tastypie import fields

from .models import Service

class ServiceResource(ModelResource):
    is_down = fields.BooleanField(attribute='is_down')
    endpoint = fields.CharField(attribute='endpoint')

    class Meta:
        queryset = Service.objects.all()
        resource_name = 'service'
        allowed_methods = ['get']
        excludes = ['force_down', 'is_crawler_enabled', 'created_at', 'edited_at']