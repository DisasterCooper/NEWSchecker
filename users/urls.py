from django.urls import path

from . import views

#  /users/

app_name = "users"

urlpatterns = [
    path('<int:user_id>/', views.RedactUser.as_view(), name='redact_user'),
        ]
