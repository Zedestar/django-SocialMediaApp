from django.urls import path
from . import views

# - The urls patterns

urlpatterns = [
    path('', views.home, name='chattings_home'),
    path('room/<int:pk>/', views.home, name='chattings_room'),
]