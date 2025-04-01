from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # après inscription, redirige vers la connexion
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def custom_login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue {user.username} !")
                return redirect('/prospects/')  # Redirection vers la liste des prospects
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {'form': form})