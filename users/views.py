from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views import View, generic
from flower.views.auth import authenticate

from .forms import UserRegisterForm, UserRedactForm
from .models import User


class Registration(View):

    def get(self, request):
        return render(request, "registration/registration.html", {"form": UserRegisterForm()})

    def post(self, request):

        form = UserRegisterForm(request.POST)

        if not form.is_valid():
            return render(request, "registration/registration.html", {"form": form})

        user = form.save(commit=False)  # Создаем объект, без сохранения в БД
        user.is_active = False
        user.save()

        return redirect("accounts:login")


class RedactUser(generic.UpdateView):
    model = User
    form_class = UserRedactForm
    pk_url_kwarg = "users_id"
    template_name = "users/redact_user.html"


def Login(request):
    if request.user.is_authenticated:
        return redirect("news:home")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("news:home")
            else:
                messages.error(request, "Username or password is incorrect")
        return render(request, "registration/login.html")


def LogOut(request):
    logout(request)
    return redirect("accounts:login")
