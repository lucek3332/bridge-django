from django.urls import re_path
from .views import room

urlpatterns = [
    re_path(r"^(?P<room_name>[\w\d-]+)/$", room, name="room"),
]
