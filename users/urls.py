from django.urls import path
from .views import register, custom_login_view


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', custom_login_view, name='login'),
]
