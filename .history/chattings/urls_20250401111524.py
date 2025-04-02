from django.urls import path
from . import views

# - The urls patterns

urlpatterns = [
    path('', views.home, name='chattings_home'),
    path('room/<int:pk>/', views.room, name='chattings_room'),
    path('create_room', views.create_room, name='chattings_create_room'),
    path('update_room/<int:pk>/', views.update_room, name='chatting_update_room'),
    path('delete_room/<int:pk>/', views.delete_room, name='chatting_delete_room'),
    path("user_profile/<str:pk>/", views.user_profile, name="user_profile_data"),
#     path('inbox_room/<str:pk>/', views.the_inbox_room, name='inbox_room'),
# ]