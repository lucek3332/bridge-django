from django.shortcuts import render
from .forms import ProfileRegisterForm, UserRegisterForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from accounts.tasks import send_mail_task
from bridge.settings import EMAIL_HOST_USER


def register_view(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileRegisterForm(request.POST)
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
