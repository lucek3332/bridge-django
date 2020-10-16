from django.urls import re_path
from django.contrib.auth.views import LoginView, logout_then_login
from .views import register_view


urlpatterns = [
    re_path(r"^login/$", LoginView.as_view(), name="login"),
    re_path(r"^register/$", register_view, name="register"),
    re_path(r"^logout/$", logout_then_login, name="logout"),
]
