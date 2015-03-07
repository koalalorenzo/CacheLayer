from tastypie.resources import ModelResource
from .models import Service

class ServiceResource(ModelResource):
    class Meta:
        queryset = Service.objects.all()
        resource_name = 'service'
        allowed_methods = ['get']