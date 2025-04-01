from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
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
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenue {user.username} !")
            return redirect('/prospects/')  # Redirection vers la liste des prospects
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe invalide.")

    return render(request, "users/login.html")