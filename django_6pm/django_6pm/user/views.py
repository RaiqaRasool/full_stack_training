from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from user.forms import ProfileForm, UserForm


def index(request):
    return render(request, "index.html")


class SignUpTemplateView(TemplateView):
    template_name = "user/signup.html"

    def get(self, request):
        user_form = UserForm(prefix="user")
        profile_form = ProfileForm(prefix="profile")
        return render(request, "user/signup.html", {"user_form": user_form, "profile_form": profile_form})

    def post(self, request):
        user_form = UserForm(request.POST, prefix="user")
        profile_form = ProfileForm(request.POST, request.FILES, prefix="profile")
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return redirect("login")
        return render(request, "user/signup.html", {"user_form": user_form, "profile_form": profile_form})


class UserLoginView(LoginView):
    template_name = "user/login.html"


class UserLogoutView(LogoutView):
    template_name = "user/logout.html"
