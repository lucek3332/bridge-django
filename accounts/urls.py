from django.urls import re_path
from django.contrib.auth.views import LoginView, logout_then_login, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import register_view, register_confirm_view
from django.urls import reverse_lazy
from .forms import CustomPasswordResetForm


urlpatterns = [
    re_path(r"^login/$", LoginView.as_view(extra_context={"section": "dashboard"}), name="login"),
    re_path(r"^register/$", register_view, name="register"),
    re_path(r"^logout/$", logout_then_login, name="logout"),
    re_path(r"^password_change/$",
            PasswordChangeView.as_view(template_name="registration/password_change_form.html",
                                       success_url=reverse_lazy("accounts:password_change_done",
                                       extra_context={"section": "dashboard"})), name="password_change"),
    re_path(r"^password_change/done/$", PasswordChangeDoneView.as_view(extra_context={"section": "dashboard"}), name="password_change_done"),
    re_path(r"^password_reset/$", PasswordResetView.as_view(form_class=CustomPasswordResetForm,
                                                            success_url=reverse_lazy("accounts:password_reset_done"),
                                                            extra_context={"section": "dashboard"}), name="password_reset"),
    re_path(r"^password_reset/done/$", PasswordResetDoneView.as_view(extra_context={"section": "dashboard"}), name="password_reset_done"),
    re_path(r"^reset/(?P<uidb64>\w+)/(?P<token>[\d\w-]+)/$",
            PasswordResetConfirmView.as_view(success_url=reverse_lazy("accounts:password_reset_complete"),
                                             extra_context={"section": "dashboard"}), name="password_reset_confirm"),
    re_path(r"^reset/done/$", PasswordResetCompleteView.as_view(extra_context={"section": "dashboard"}), name="password_reset_complete"),
    re_path(r"^register_confirm/(?P<uidb64>\d+)/(?P<token>[\w\d-]+)/$", register_confirm_view, name="register_confirm"),
]
