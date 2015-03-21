import re

import logging
logger = logging.getLogger(__name__)

from django.contrib.auth.models import User
from django.db import models
from django.core.cache import cache
from django.test import Client

try:
    import urlparse
except:
    from urllib.parse import urlparse

from tld import get_tld

from .tasks import download_content


class Service(models.Model):
    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

    name = models.CharField("Name", max_length=50)
    domain = models.CharField("Domain", max_length=60)

    descrition = models.TextField(null=True, blank=True)

    store_days = models.IntegerField("Days to keep data", default=7)
    check_period = models.IntegerField("Period of downtime", default=60)
    request_timeout = models.IntegerField("Request timeout", default=30)
    cache_duration = models.IntegerField("Cache expiration", default=60)

    is_enabled = models.BooleanField(default=False)
    force_down = models.BooleanField(default=False)

    is_crawler_enabled = models.BooleanField(default=False)
    crawled_at = models.DateTimeField(blank=True, null=True)

    created_by = models.ForeignKey(User, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    @property
    def endpoint(self):
        return self.get_absolute_url()

    @property
    def is_down(self):
        if self.force_down:
            return True
        return cache.get("status:%s" % self.domain, False)

    @is_down.setter
    def is_down(self, value):
        status = "is down!" if value else "is up!"
        logger.info("[service:%s] %s" % (self.domain, status))

        return cache.set("status:%s" % self.domain, value, self.check_period)

    # Save the content for longer

    def get_storage_key(self, request):
        """ Get the key to use in the cache """
        request_hash = hash(frozenset(request.REQUEST.items()))
        path = self.__extract_path(request.path)

        return 'request:{service}:{path}:{method}:{hash}'.format(
            service=self.domain,
            path=path,
            method=request.method,
            hash=request_hash,
        )

    def store_content(self, request, content):
        """ Save the content in the storage """
        seconds = 60 * 60 * 24 * self.store_days
        cache.set(self.get_storage_key(request), content, seconds)

        logger.debug("{key} Saved for {days} days".format(
            key=self.get_storage_key(request),
            days=self.store_days
        ))

    def get_stored_content(self, request):
        """ Get the content from the storage """
        logger.debug("{key} Requested from cache".format(
            key=self.get_storage_key(request),
        ))
        return cache.get(self.get_storage_key(request), None)

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
        """ Save the content, based on the request, in cache """
        if self.cache_duration <= 0:
            return

        cache.set(self.get_cache_key(request), content, self.cache_duration)

        logger.debug("{key} Cached for {seconds} seconds".format(
            key=self.get_cache_key(request),
            seconds=self.cache_duration
        ))

    def get_cached_content(self, request):
        """ Get the content, based on the request from the cache """
        logger.debug("{key} Requested from cache".format(
            key=self.get_cache_key(request),
        ))
        return cache.get(self.get_cache_key(request), None)

    def __extract_path(self, request_path):
        path = request_path.replace(self.get_absolute_url(), "")
        if not path:
            return "/"
        return path

    def __make_remote_request(self, request):
        """ This method is making the "reverse_proxy" happen. """

        timeout = int(self.request_timeout)
        extra_url = self.__extract_path(request.path)
        base_url = "{}://{}/".format(request.scheme, self.domain)
        the_url = '/'.join(s.strip('/') for s in [base_url, extra_url])

        logger.debug("{key} Downloading {url}".format(
            key=self.get_storage_key(request),
            url=the_url,
        ))

        # See: http://stackoverflow.com/questions/3889769/how-can-i-get-all-the-request-headers-in-django
        regex = re.compile('^HTTP_')
        headers = dict()
        for (header, value) in request.META.items():
            if header.startswith('HTTP_'):
                header_new = regex.sub('', header).replace("_", "-")
                headers[header_new] = value

        task = download_content.delay(
            method=request.method,
            url=the_url,
            timeout=timeout,
            headers=headers
        )
        return task.get(timeout=timeout)

    # The core methods:

    def get_remote_content(self, request):
        """Call the server and return the content"""
        logger.debug("{key} requested from server".format(
            key=self.get_storage_key(request),
        ))

        content = self.__make_remote_request(request)

        try:
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
        """
            This method will check the status, the cache and then
            decide from where get the content and download it from there.
            it will return the content object that is a response inside a
            dictionary with this structure:

            {
                "content": the response,
                "content-type": its content type,
                "headers": its headers,
                "created": string of the date when it was downloaded.
            }
        """
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
        """ Download the URL and set, if needed, the service as Down """
        client = Client()
        test_request = client.get(self.get_absolute_url())

        if test_request.has_header("X-CacheLayer-Status"):
            return test_request["X-CacheLayer-Status"] == "GOT", test_request
        return False, test_request

    def get_absolute_url(self):
        return "/pub/%s/" % (self.domain)

    def save(self, *args, **kwargs):
        if "http" in self.domain:
            self.domain = get_tld(self.domain)
        return super(Service, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.domain)

    def __unicode__(self):
        return u"{}".format(self.__str__())

    @classmethod
    def from_url_to_cachelayer_path(cls, url):
        domain = get_tld(url)
        return url[url.index(domain):]
