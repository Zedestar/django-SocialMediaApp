from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/room_chat/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]
