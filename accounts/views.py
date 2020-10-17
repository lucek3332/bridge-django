from django.shortcuts import render
from .forms import ProfileRegisterForm, UserRegisterForm
from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import EmailMessage


def register_view(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileRegisterForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_cd = user_form.cleaned_data
            prof_cd = profile_form.cleaned_data
            new_user = User.objects.create(**user_cd)
            new_user.set_password(prof_cd['password'])
            #new_user.is_active = False
            new_user.save()
            profile = Profile.objects.create(user=new_user, photo=prof_cd["photo"], description=prof_cd["description"])
            profile.save()
            #email_subject = "Rejestracja na stronie brydża!"
            #email_message = "Gratulacje {}! Twoja rejestracja na stronie brydża została zakończona pomyślnie. Żeby się zalogować kliknij poniższy link.".format(new_user.first_name)
            #email = EmailMessage(email_subject, email_message, to=[new_user.email])
            #email.send()
            return render(request, "registration/register_done.html", {"user": new_user,
                                                                       "profile": profile})
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileRegisterForm()
    return render(request, "registration/register.html", {"user_form": user_form,
                                                          "profile_form": profile_form})
