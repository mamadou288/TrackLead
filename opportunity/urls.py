from django.urls import path
from .views import add_opportunity, opportunity_list, opportunity_detail, opportunity_update, opportunity_delete, create_opportunity

urlpatterns = [
    path('', opportunity_list, name='opportunity-list'),
    path('add/', create_opportunity, name='create-opportunity'),
    path('add/<int:prospect_id>/', add_opportunity, name='add-opportunity'),
    path('<int:pk>/', opportunity_detail, name='opportunity-detail'),
    path('<int:pk>/edit/', opportunity_update, name='opportunity-edit'),
    path('<int:pk>/delete/', opportunity_delete, name='opportunity-delete'),
]