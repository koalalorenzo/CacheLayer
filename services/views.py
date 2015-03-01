from datetime import datetime

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

def get_data(request, service_reference, extra_url=None):
    """"""
    service = get_object_or_404(Service, pk=service_reference)
    
    content = service.content(request)
    if not content:
        response = HttpResponseServerError("Service not available or cache expired")
        response["X-OpenData-Created"] = datetime.now()

    else:
        response = HttpResponse(content["content"], content_type=content["content-type"])
        
        for header_key, header_value in content["headers"].iteritems():
            if header_key.lower() in HOP_BY_HOP_HEADERS:
                continue
            response[header_key] = header_value
        
        response["X-OpenData-Created"] = content['created']
        
    response["X-OpenData-Status"] = "HIT" if service.is_down else "LIVE"
    return response