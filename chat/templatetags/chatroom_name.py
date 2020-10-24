from django import template

register = template.Library()

def chatroom_name(request):
    addr = request.scope['path']
    user1_id = request.user.pk
    user2_id = int(addr.split("/")[-2])
    return "chatroom-{}-{}".format(min(user1_id, user2_id), max(user1_id, user2_id))

register.filter('chatroom_name', chatroom_name)