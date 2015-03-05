from datetime import datetime

import logging
logger = logging.getLogger(__name__)

from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseServerError

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
        response = HttpResponseServerError("Service not available or cache expired")
        response["X-CacheLayer-Created"] = datetime.now()

    else:
        response = HttpResponse(content["content"], content_type=content["content-type"])
        
        for header_key, header_value in content["headers"].iteritems():
            if header_key.lower() in HOP_BY_HOP_HEADERS:
                continue
            response[header_key] = header_value
        
        response["X-CacheLayer-Created"] = content['created']
        
    response["X-CacheLayer-Status"] = "HIT" if service.is_down else "LIVE"
    return response
