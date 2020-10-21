from django.shortcuts import render
from .forms import ProfileRegisterForm, UserRegisterForm, EditUserForm, EditProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .models import Profile
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from accounts.tasks import send_mail_task
from bridge.settings import EMAIL_HOST_USER
from django.contrib import messages
from django.dispatch import receiver


def register_view(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileRegisterForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_cd = user_form.cleaned_data
            prof_cd = profile_form.cleaned_data
            new_user = User.objects.create(**user_cd)
            new_user.set_password(prof_cd['password'])
            new_user.is_active = False
            new_user.save()
            profile = Profile.objects.create(user=new_user, photo=prof_cd["photo"], description=prof_cd["description"])
            profile.save()
            token = PasswordResetTokenGenerator().make_token(new_user)
            uid = new_user.pk
            protocol = request.build_absolute_uri().split(":")[0]
            domain = get_current_site(request)
            email_subject = "Aktywacja konta"
            email_message = "Witaj {}! W celu aktywacji konta kliknij poniższy link. " \
                            "{}://{}/accounts/register_confirm/{}/{}".format(new_user.first_name, protocol, domain, uid, token)
            send_mail_task.delay(email_subject, email_message, EMAIL_HOST_USER, [new_user.email])
            return render(request, "registration/register_done.html", {"user": new_user,
                                                                       "profile": profile,
                                                                       "section": "dashboard"})
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileRegisterForm()
    return render(request, "registration/register.html", {"user_form": user_form,
                                                          "profile_form": profile_form,
                                                          "section": "dashboard"})


def register_confirm_view(request, uidb64, token):
    user = get_object_or_404(User, pk=uidb64)
    generator_token = PasswordResetTokenGenerator()
    validtoken = False
    if generator_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        validtoken = True
    return render(request, "registration/register_confirm.html", {"validtoken": validtoken,
                                                                  "section": "dashboard"})


@login_required
def edit_profile_view(request):
    if request.method == "POST":
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(data=request.POST, files=request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            messages.info(request, "Zmiany zostały zapisane")
            user_form.save()
            profile_form.save()
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)
    return render(request, "users/edit.html", {"user_form": user_form,
                                               "profile_form": profile_form,
                                               "section": "account"})


@login_required
def profile_view(request, user_id):
    user_profile = get_object_or_404(User, pk=user_id)
    return render(request, "users/profile.html", {"user_profile": user_profile,
                                                  "section": "dashboard"})


@receiver(user_logged_in)
def get_online(sender, **kwargs):
    user = kwargs["user"]
    profile = get_object_or_404(Profile, user=user)
    profile.is_online = True
    profile.save()


@receiver(user_logged_out)
def get_offline(sender, **kwargs):
    user = kwargs["user"]
    profile = get_object_or_404(Profile, user=user)
    profile.is_online = False
    profile.save()
