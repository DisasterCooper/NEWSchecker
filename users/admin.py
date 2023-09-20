from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import User
from .forms import UserRegisterForm


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    form = UserRegisterForm
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
    ]
    search_fields = ["username", "email", ]
