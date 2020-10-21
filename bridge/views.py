from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def dashboard_view(request):
    user = request.user
    friends = user.profile.friends.all()
    if not friends:
        messages.info(request, "Nie masz jeszcze żadnych znajomych.")
    return render(request, "dashboard.html", {"section": "dashboard",
                                              "friends": friends})
