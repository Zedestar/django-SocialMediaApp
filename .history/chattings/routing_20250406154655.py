from django.urls import path
from . import consumers


websocket_urlPatterns = [
    path('ws/room_chat/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]