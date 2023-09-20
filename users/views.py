from django.shortcuts import render, redirect
from django.views import View

from .forms import UserRegisterForm


class Registration(View):

    def get(self, request):
        return render(request, "users/registration.html", {"form": UserRegisterForm()})

    def post(self, request):

        form = UserRegisterForm(request.POST)

        if not form.is_valid():
            return render(request, "users/registration.html", {"form": form})

        user = form.save(commit=False)  # Создаем объект, без сохранения в БД
        user.is_active = False
        user.save()

        return redirect("")
