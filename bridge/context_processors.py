def friends(request):
    if not request.user.is_authenticated:
        friends = None
    else:
        friends = request.user.profile.friends.all()
    return {"friends": friends}