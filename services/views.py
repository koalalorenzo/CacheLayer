from datetime import datetime

import logging
logger = logging.getLogger(__name__)

from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render

from .models import Service

HOP_BY_HOP_HEADERS = [
    "connection",
    "content-encoding",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
]


def get_data(request, domain, extra_url=None):
    """"""

    service = get_object_or_404(Service, domain=domain)

    content = service.get_content(request)
    if not content:
        response = HttpResponseServerError(
            "Service not available or cache expired"
        )
        response["X-CacheLayer-Created"] = datetime.now()

    else:
        response = HttpResponse(
            content["content"], content_type=content["content-type"]
        )

        for header_key in content["headers"]:
            if header_key.lower() in HOP_BY_HOP_HEADERS:
                continue

            # Python 3 and 2 support:
            response[header_key] = content["headers"][header_key]

        response["X-CacheLayer-Created"] = content['created']

    response["X-CacheLayer-Status"] = "HIT" if service.is_down else "GOT"
    return response


def service_list(request):
    return render(request, 'services-list.html')
