from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    photo = models.ImageField(upload_to="profiles/", blank=True)
    description = models.TextField(blank=True)
    is_online = models.BooleanField(default=False)
    chat_status = models.IntegerField(default=0)
    play_status = models.BooleanField(default=False)
    friends = models.ManyToManyField("self", symmetrical=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-is_online", "user")

    def get_absolute_url(self):
        return reverse("accounts:profile", args=[str(self.user.pk)])


    def __str__(self):
        return "Profil - {}".format(self.user)

    def __repr__(self):
        return "Profil - {}".format(self.user)
