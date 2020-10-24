from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from accounts.views import search_users


def room(request, room_name):
    users_id = list(map(int, room_name.split("-")[1:]))
    for u_id in users_id:
        if u_id != request.user.pk:
            other_user = get_object_or_404(User, pk=u_id)
    if "search" in request.GET:
        query = request.GET.get("search")
        users = search_users(query)
        return render(request, "search.html", {"section": "dashboard",
                                               "search_result": users})
    return render(request, "chat/room.html", {"room_name": room_name,
                                              "section": "dashboard",
                                              "other_user": other_user})
