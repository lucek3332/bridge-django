from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def string_to_list(string):
    lst = string.split(",")
    return lst


def list_to_string(lst):
    return ",".join(item for item in lst)


class ListField(models.Field):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value

        return string_to_list(value)

    def to_python(self, value):
        if isinstance(value, list):
            return value

        if value is None:
            return value

        return string_to_list(value)

    def get_prep_value(self, value):
        return list_to_string(value)


class Hand(models.Model):
    south = ListField()
    north = ListField()
    east = ListField()
    west = ListField()


class Boards(models.Model):
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
