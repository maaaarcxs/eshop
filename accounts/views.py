from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            login(request, user)  
            messages.success(request, f"Добро пожаловать, {user.username}!")
            return redirect("home")
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect("register")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Вы вошли как {user.username}")
            return redirect("home")
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect("login")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Вы вышли из системы")
    return redirect("login")
