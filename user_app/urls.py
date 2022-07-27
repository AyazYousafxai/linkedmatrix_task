from django.urls import path
from .views import user_info, group_user_access

urlpatterns = [
    path("ip_user/", user_info, name="ip_user"),
    path("group/", group_user_access, name="group_user"),
]
