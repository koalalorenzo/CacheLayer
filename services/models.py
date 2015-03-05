from datetime import datetime

import urlparse
import requests
import socket

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.core.cache import cache
from django.http import HttpResponse, HttpRequest
from django.test import Client

class Service(models.Model):
    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

    name = models.CharField("Name", max_length=50)
    domain = models.CharField("Domain", null=True, blank=True, max_length=60)

    descrition = models.TextField(null=True, blank=True)


    store_days = models.IntegerField("Store duration (in days)", default=7)
    check_period = models.IntegerField("Status period (in seconds)", default=60)
    request_timeout = models.IntegerField("Request timeout (in seconds)", default=30)
    cache_duration = models.IntegerField("Cache duration (in seconds)", default=60)
    
    is_enabled = models.BooleanField(default=False)
    is_crawler_enabled = models.BooleanField(default=False)
    force_down = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    crawled_at = models.DateTimeField(blank=True, null=True)

    @property
    def is_down(self):
        if self.force_down: 
            return True
        return cache.get("status:%s" % self.domain, False)

    @is_down.setter
    def is_down(self, value):
        status = "is down!" if value else "is up!"
        logger.info("[service:%s] %s" % (self.domain, status) )

        return cache.set("status:%s" % self.domain, value, self.check_period)        

    # Save the content for longer

    def get_storage_key(self, request):
        """Get the key to use in the cache"""
        request_hash = hash(frozenset(request.REQUEST.items()))
        path = self.__extract_path(request.path)

        return 'request:{service}:{path}:{method}:{hash}'.format(
            service=self.domain, 
            path=path,
            method=request.method, 
            hash=request_hash,
        )

    def get_stored_content(self, request):
        logger.debug("{key} Requested from cache".format(
            key=self.get_storage_key(request),
        ))
        return cache.get(self.get_storage_key(request), None)

    def store_content(self, request, content):
        seconds = 60*60*24 * self.store_days
        cache.set(self.get_storage_key(request), content, seconds)
        
        logger.debug("{key} Saved for {days} days".format(
            key=self.get_storage_key(request),
            days=self.store_days
        ))

    # Save the content for few seconds

    def get_cache_key(self, request):
        """Get the key to use in the cache"""
        request_hash = hash(frozenset(request.REQUEST.items()))
        path = self.__extract_path(request.path)

        return 'cache:{service}:{path}:{method}:{hash}'.format(
            service=self.domain, 
            path=path,
            method=request.method, 
            hash=request_hash,
        )

    def cache_content(self, request, content):
        if self.cache_duration <= 0:
            return 

        cache.set(self.get_cache_key(request), content, self.cache_duration)
        
        logger.debug("{key} Cached for {seconds} seconds".format(
            key=self.get_cache_key(request),
            seconds=self.cache_duration
        ))

    def get_cached_content(self, request):
        logger.debug("{key} Requested from cache".format(
            key=self.get_cache_key(request),
        ))
        return cache.get(self.get_cache_key(request), None)


    # Tools

    def __extract_path(self, request_path):
        return request_path.replace(self.get_absolute_url(), "")


    def __make_remote_request(self, request):
        """
            This method is making the "reverse_proxy" happen.
        """
        requestor = getattr(requests, request.method.lower())
        try:
            body = request.body
            has_body = True
        except:
            has_body = False

        timeout = int(self.request_timeout)
        extra_url = self.__extract_path(request.path)
        base_url = "{}://{}/".format(request.scheme, self.domain)
        the_url = urlparse.urljoin(base_url, extra_url)

        logger.debug("{key} Downloading {url}".format(
            key=self.get_storage_key(request),
            url=the_url,
        ))

        socket.setdefaulttimeout(timeout)
        if has_body:
            proxied_response = requestor(
                the_url, timeout=timeout,
                data=request.body, files=request.FILES
            )
        else:
            proxied_response = requestor(the_url, timeout=int(timeout))

        return proxied_response

    # The core methods:

    def get_remote_content(self, request):
        """Call the server and return the content"""
        logger.debug("{key} requested from server".format(
            key=self.get_storage_key(request),
        ))

        try:
            response = self.__make_remote_request(request)
            content = {
                "content": response.content,
                "content-type": response.headers.get('content-type'),
                "headers": response.headers,
                "created": datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
            }
            self.is_down = False
        except:
            self.is_down = True
            return False, None

        logger.debug("{key} requested successful from server".format(
            key=self.get_cache_key(request),
        ))

        self.store_content(request, content)
        return True, content

    def get_content(self, request, force=False):
        if self.is_down and not force:
            return self.get_stored_content(request)

        if self.cache_duration > 0:
            # Return the cached content if available.
            cached_content = self.get_cached_content(request)
            if cached_content:
                return cached_content

        success_status, content = self.get_remote_content(request)
        if success_status:
            self.store_content(request, content)
            self.cache_content(request, content)
            return content
        
        if force:
            return content
        
        return self.get_stored_content(request)

    def ping(self):
        """ Ping the URL and set, if needed, the service as Down """
        client =  Client()
        test_request = client.get(self.get_absolute_url())

        if test_request.has_header("ODCACHE-STATUS"):
            return test_request["ODCACHE-STATUS"] == "LIVE"
        return False, test_request

    def __str__(self):
        return "{}".format(self.domain) 
    
    def __unicode__(self):
        return u"{}".format(self.domain) 


    def get_absolute_url(self):
        return "/pub/%s/" % (self.domain)
