from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.views import search_users
from django.contrib.auth.models import User
from chat.models import Message


@login_required
def dashboard_view(request):
    notifications = []
    for user in User.objects.all():
        if Message.objects.filter(author=user.username, to=request.user.username, readed=False).exists():
            notifications.append((user, "chatroom-{}-{}".format(min(request.user.pk, user.pk), max(request.user.pk, user.pk))))
    if "search" in request.GET:
        query = request.GET.get("search")
        users = search_users(query)
        return render(request, "search.html", {"section": "dashboard",
                                               "search_result": users,
                                               "notifications": notifications})
    return render(request, "dashboard.html", {"section": "dashboard",
                                              "notifications": notifications})
