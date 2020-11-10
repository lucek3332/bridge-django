from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.views import search_users
from django.contrib.auth.models import User
from chat.models import Message
from .tasks import play_task


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


@login_required
def play_view(request):
    profile = request.user.profile
    user = request.user
    if not request.GET and not profile.play_status:
        profile.play_status = True
        profile.save()
        play_task.delay(user.username)
    return render(request, "play.html", {"section": "play",
                                         "status_play": profile.play_status})
