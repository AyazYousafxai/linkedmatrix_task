from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from user_app.get_user_ip import ip_address
from rest_framework.response import Response
import json
from rest_framework.renderers import JSONRenderer
from rest_framework import status
import datetime
import logging


logging.basicConfig(level=logging.INFO)


def rate_limit(user, time_limit, call_limit):
    if cache.get(user):
        total_calls = cache.get(user)
        logging.info("total_calls %s", total_calls)
        logging.info(total_calls)
        if total_calls > call_limit:
            return False
        else:
            cache.set(user, total_calls + 1, cache.ttl(user))
            return True
    cache.set(user, 2, time_limit)

    return True


def set_response(response):
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = "application/json"
    response.renderer_context = {}
    response.render()
    return response


class LogTime(MiddlewareMixin):
    def process_request(self, request):
        ip = ip_address(request)
        now = datetime.datetime.now()
        logging.info("IP Address of user %s and time %s", ip, now)
        is_allowed = False
        if "group" in request.path:
            data = json.loads(request.body)
            if data["user_type"] == "Gold":
                is_allowed = rate_limit(data["user_id"], 60, 10)
            elif data["user_type"] == "Silver":
                is_allowed = rate_limit(data["user_id"], 60, 5)
                print(is_allowed)
            elif data["user_type"] == "Bronze":
                is_allowed = rate_limit(data["user_id"], 60, 2)
            elif data["user_type"] == "No Group":
                is_allowed = rate_limit(data["user_id"], 60, 1)
            if not is_allowed:
                response = Response(
                    "ratelimit exceed try again after "
                    + str(cache.ttl(data["user_id"])),
                    status=status.HTTP_403_FORBIDDEN,
                )
                return set_response(response)
