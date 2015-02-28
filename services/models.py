from django.db import models
from django.core.cache import cache
from django.http import HttpResponse, HttpRequest
from django.test import Client

import urlparse
import requests


class Service(models.Model):
    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

    name = models.CharField("Service Name", max_length=50)
    descrition = models.TextField(null=True, blank=True)

    base_url = models.URLField(null=True, blank=True)

    cache = models.IntegerField("Cache duration (in seconds)", default=300)
    check = models.IntegerField("Check period", default=60)
    request_timeout = models.IntegerField("HTTP request timeout", default=30)

    is_enabled = models.BooleanField(default=False)
    force_down = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    @property
    def is_down(self):
        if self.force_down: 
            return True
        return cache.get("service_%s_is_down" % self.pk, False)

    @is_down.setter
    def is_down(self, value):
        return cache.set("service_%s_is_down" % self.pk, value, self.check)        

    def save_cached_content(self, request, content):
        cache.set(self.get_cache_key(request), content, self.cache)

    def get_cached_content(self, request):
        return cache.get(self.get_cache_key(request), None)

    def __make_remote_request(self, request):
        requestor = getattr(requests, request.method.lower())
        try:
            body = request.body
            has_body = True
        except:
            has_body = False

        timeout = int(self.request_timeout)
        extra_url = request.path.replace(self.get_absolute_url(), "")
        the_url = urlparse.urljoin(self.base_url, extra_url)

        if has_body:
            proxied_response = requestor(
                the_url, timeout=timeout,
                data=request.body, files=request.FILES
            )
        else:
            proxied_response = requestor(the_url, timeout=int(timeout))

        return proxied_response

    def get_remote_content(self, request):
        """Call the server and return the content"""
        try:
            response = self.__make_remote_request(request)
            content = {
                "content": response.content,
                "content-type": response.headers.get('content-type'),
                "headers": response.headers,
            }
            self.is_down = False
        except:
            self.is_down = True
            return False, None

        self.save_cached_content(request, content)
        return True, content

    def content(self, request, force=False):
        if self.is_down and not force:
            return self.get_cached_content(request)

        success_status, content = self.get_remote_content(request)
        if success_status:
            self.save_cached_content(request, content)
            return content
        elif force:
            return content
        
        return self.get_cached_content(request)
    
    def get_cache_key(self, request):
        """Get the key to use in the cache"""
        final_hash = hash(request.method)
        final_hash += hash(frozenset(request.REQUEST.items()))
        final_hash += hash(frozenset(request.COOKIES.items()))

        return 'service_%s_request_%s' % (self.pk, final_hash)

    def ping(self):
        """ Ping the URL and set, if needed, the service as Down """
        client =  Client()
        test_request = client.get(self.get_absolute_url())

        if test_request.has_header("ODCACHE-STATUS"):
            return test_request["ODCACHE-STATUS"] == "LIVE"
        return False, test_request

    def __str__(self):
        return "%s %s" % (self.name, self.base_url[:30]) 
    
    def get_absolute_url(self):
        return "/%s" % self.pk
