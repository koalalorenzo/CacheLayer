from __future__ import absolute_import

from celery import shared_task

from datetime import datetime
import random
import requests


@shared_task
def add(x):
    return x + random.randint(1, 100)


@shared_task
def download_content(*args, **kwargs):
    """ This method is making the "reverse_proxy" happen. """
    method = kwargs.get("method", "get")
    url = kwargs.get("url", "")
    timeout = kwargs.get("timeout", 60)
    headers = kwargs.get("headers", {})

    requestor = getattr(requests, method.lower())
    response = requestor(
        url,
        headers=headers,
        timeout=int(timeout),
        allow_redirects=False,
    )

    content = {
        "content": response.content,
        "content-type": response.headers.get('content-type'),
        "headers": response.headers,
        "created": datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    }

    return content
