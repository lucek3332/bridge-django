from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.views import search_users


@login_required
def dashboard_view(request):
    if "search" in request.GET:
        query = request.GET.get("search")
        users = search_users(query)
        return render(request, "search.html", {"section": "dashboard",
                                               "search_result": users})
    return render(request, "dashboard.html", {"section": "dashboard"})
