from django.shortcuts import render, get_object_or_404
from .models import Board
from django.contrib.auth.models import User


def board_list_view(request):
    boards = Board.get_last_boards(request.user)
    return render(request, "boards/list.html", {"section": "history",
                                                "boards": boards})


def board_detail_view(request, player, board_id):
    board = get_object_or_404(Board, unique_id=board_id, player=request.user)
    return render(request, "boards/detail.html", {"section": "history",
                                                  "board": board})
