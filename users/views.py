from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm


def login_user(request):

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Usuário ou Senha incorretos')
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})


def logout_user(request):

    logout(request)
    return redirect('login')


def register_user(request):

    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterUserForm()

    return render(request, 'user/register.html', {'form': form,})


def user_info(request):
    if request.method == 'POST':
        request.user.email = request.POST['email']
        request.user.save()

    return render(request, 'user/info.html', {})
