from django.urls import path
from .views import custom_login_view, custom_logout_view, register_with_invitation, send_invitation, profile_view, edit_profile_view

urlpatterns = [
    path('login/', custom_login_view, name='login'),
    path('logout/', custom_logout_view, name='logout'),
    path('register_with_invitation/<str:token>/', register_with_invitation, name='register_with_invitation'),
    path('send_invitation/', send_invitation, name='send_invitation'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit-profile'),
]
