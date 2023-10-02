from django.urls import path

from . import views
from users.views import Login, LogOut

#  /users/

app_name = "users"

urlpatterns = [
    path("<int:users_id>/", views.RedactUser.as_view(), name="redact_user"),
    path("login/", Login, name="login"),
    path("logout/", LogOut, name="logout"),
        ]
