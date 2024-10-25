from django.urls import re_path
from . import views

urlpatterns = [
    re_path("login/", views.login, name="login"),
    re_path("signup/", views.signup, name="signup"),
    re_path("logout/", views.logout, name="logout"),
]
