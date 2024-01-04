from django.urls import path
from django.contrib.auth.views import LogoutView

from user.views import *

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("signup/", SignUpTemplateView.as_view(), name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="profile")
]
