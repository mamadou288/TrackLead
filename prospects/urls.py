from django.urls import path
from .views import prospect_list, prospect_create, prospect_detail, prospect_update, prospect_delete

urlpatterns = [
    path('', prospect_list, name='prospect-list'),
    path('create/', prospect_create, name='prospect-create'),
    path('<int:pk>/', prospect_detail, name='prospect-detail'),
    path('<int:pk>/edit/', prospect_update, name='prospect-update'),
    path('<int:pk>/delete/', prospect_delete, name='prospect-delete'),
]
