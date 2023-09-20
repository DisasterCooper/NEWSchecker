from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserRedactForm(UserChangeForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = "__all__"
