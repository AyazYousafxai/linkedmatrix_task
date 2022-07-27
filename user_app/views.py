from rest_framework.decorators import api_view
from rest_framework.response import Response
from .get_user_ip import ip_address
from django.core.cache import cache
from rest_framework import status
import logging


def rate_limit(current_ip):
    logging.info(cache.ttl(current_ip))
    if cache.get(current_ip):
        total_calls = cache.get(current_ip)
        logging.info("total calls %s", total_calls)
        if total_calls > 5:
            return False
        else:
            cache.set(current_ip, total_calls + 1, cache.ttl(current_ip))
            return True
    cache.set(current_ip, 1, 60)

    return True


@api_view(["Get"])
def user_info(request):
    ip = ip_address(request)
    is_allowed = rate_limit(ip)
    if not is_allowed:
        return Response(
            "limit exceed please try after " + str(cache.ttl(ip)),
            status=status.HTTP_403_FORBIDDEN,
        )
    return Response("Happy", status=status.HTTP_200_OK)


@api_view(["Post"])
def group_user_access(request):
    return Response("Happy", status=status.HTTP_200_OK)


# Create your views here.
