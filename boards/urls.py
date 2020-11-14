from django.urls import re_path
from .views import board_list_view, board_detail_view


urlpatterns = [
    re_path(r"^$", board_list_view, name="board_list"),
    re_path(r"^(?P<player>[\w\d]+)/(?P<board_id>[\d-]+)$", board_detail_view, name="board_detail"),
]
