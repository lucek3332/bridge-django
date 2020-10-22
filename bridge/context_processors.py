def friends(request):
    if not request.user.is_authenticated:
        friends_list = None
    else:
        friends_list = request.user.profile.friends.all()
    return {"friends": friends_list}
