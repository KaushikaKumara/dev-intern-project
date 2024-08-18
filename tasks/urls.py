from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),  # Ensure this matches your view
    path('add-task/', views.add_task, name='add_task'),  # Ensure these match your view names
    path('dashboard/', views.dashboard, name='dashboard'),
]
