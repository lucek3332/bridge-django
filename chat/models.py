from django.db import models
from django.db.models import Q



class Message(models.Model):
    author = models.CharField(max_length=255)
    to = models.CharField(max_length=255)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created", )

    # Get 20 last massages in specific chatroom from database
    @staticmethod
    def get_last_messages(user1, user2):
        return Message.objects.filter((Q(author=user1) & Q(to=user2)) | (Q(author=user2) & Q(to=user1))).order_by("-created")[:20]
