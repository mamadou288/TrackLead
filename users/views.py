from django.shortcuts import render, redirect
from .forms import InvitedUserCreationForm, InvitationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Invitation
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
# Create your views here.

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

@login_required
def custom_logout_view(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('login')

def register_with_invitation(request, token):
    invitation = get_object_or_404(Invitation, token=token, is_used=False)

    if request.method == 'POST':
        form = InvitedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = invitation.email
            user.company = invitation.company
            user.role = invitation.role
            user.save()

            invitation.is_used = True
            invitation.save()

            return redirect('login')
    else:
        form = InvitedUserCreationForm()

    return render(request, 'users/register_with_invite.html', {
        'form': form,
        'invitation': invitation
    })


@login_required
def send_invitation(request):
    if not request.user.role in ['admin', 'manager']:
        return HttpResponseForbidden("Vous n'avez pas la permission d'envoyer des invitations.")

    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.company = request.user.company  # lie à l’entreprise de l’émetteur
            invitation.save()
            return render(request, 'users/invitation_sent.html', {'invitation': invitation})
    else:
        form = InvitationForm()

    return render(request, 'users/send_invitation.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

@login_required
def profile_view(request):
    user = request.user
    company_members = None

    if user.role in ['manager', 'admin']:
        User = get_user_model()
        company_members = User.objects.filter(company=user.company)

    return render(request, 'users/profile.html', {
        'user': user,
        'company_members': company_members,
    })

from .forms import UserProfileForm

@login_required
def edit_profile_view(request):
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès.")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'users/edit_profile.html', {'form': form})
