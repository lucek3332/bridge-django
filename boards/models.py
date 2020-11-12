from django.db import models
from django.contrib.auth.models import User
from .fields import ListField


class Hand(models.Model):
    south = ListField()
    north = ListField()
    east = ListField()
    west = ListField()


class Board(models.Model):
    unique_id = models.CharField(max_length=100)
    player = models.ForeignKey(User, related_name="boards", on_delete=models.CASCADE)
    table = models.PositiveIntegerField()
    south_player = models.CharField(max_length=50)
    north_player = models.CharField(max_length=50)
    east_player = models.CharField(max_length=50)
    west_player = models.CharField(max_length=50)
    hands = models.ForeignKey(Hand, related_name="board", on_delete=models.CASCADE)
    bidding = ListField()
    tricks = ListField()
    contract = models.CharField(max_length=10)
    final_result = models.CharField(max_length=40)
    score = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created", )
