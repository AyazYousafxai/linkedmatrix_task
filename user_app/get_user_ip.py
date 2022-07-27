def ip_address(request):
    request_from = request.META.get("HTTP_X_FORWARED_FOR")
    if request_from:
        ip = request_from.split(",")[1].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
