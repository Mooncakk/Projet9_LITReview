from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from accounts.models import User


class CustomSignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields


def signup(request):

    context = {}
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Bienvenue')
        else:
            context['errors'] = form.errors

    form = CustomSignupForm()
    context['form'] = form

    return render(request, 'signup.html', context=context)


def log_user(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,f"Bienvenue {user}")
            return redirect('/flux/')
        else:
            print(request.user)
            messages.success(request, "Utilisateur ou mot de passe incorrect")
            return redirect('/login/')
    return render(request, 'login.html')


def logout_user(request):

    logout(request)
    messages.success(request, 'Vous avez été déconnecté')
    return redirect('/login/')


