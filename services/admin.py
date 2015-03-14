from django.contrib import admin
from .models import Service


def force_services_down(self, request, queryset):
    """
        Mark services as up or down.
    """
    for obj in queryset:
        obj.is_down = True


def check_if_down(self, request, queryset):
    """
        Check if a service is down by ping
    """
    for obj in queryset:
        obj.ping()


class ServiceAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'edited_at', 'crawled_at']
    raw_id_fields = ['created_by']

    list_display = [
        'domain', 'is_down', 'store_days', 'check_period', 'request_timeout',
    ]

    list_filter = ['created_at', 'crawled_at']
    search_fields = [
        'name', 'description', 'domain', 'created_by__email',
    ]

    actions = [
        force_services_down,
        check_if_down,
    ]


admin.site.register(Service, ServiceAdmin)
