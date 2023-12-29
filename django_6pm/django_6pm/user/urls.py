from django.urls import path

from user.views import *

urlpatterns = [
    path("", index, name="home"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("signup/", SignUpTemplateView.as_view(), name="signup"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
