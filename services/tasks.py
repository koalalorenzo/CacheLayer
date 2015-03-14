from __future__ import absolute_import

from celery import shared_task

import random
import requests


@shared_task
def add(x):
    return x + random.randint(1, 100)


@shared_task
def download_content(request, url, timeout):
    """ This method is making the "reverse_proxy" happen. """
    import socket

    requestor = getattr(requests, request.method.lower())
    try:
        request.body  # Checkign if it has the body method
        has_body = True
    except:
        has_body = False

    socket.setdefaulttimeout(timeout)
    if has_body:
        proxied_response = requestor(
            url, timeout=timeout,
            data=request.body, files=request.FILES
        )
    else:
        proxied_response = requestor(url, timeout=int(timeout))

    return proxied_response
