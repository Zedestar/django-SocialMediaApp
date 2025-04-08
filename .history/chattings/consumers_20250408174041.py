from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from .models import Messages, Room
# from django.conf import settings
from django.contrib.auth import get_user_model

# - Creating the consumers



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room_name']
        profile_url = data['profile_url']
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'room_name':room,
                'profile_url': profile_url
            }
        )
        
        await self.save_the_message(username, message, room)
        
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        room_name = event['room_name']
        profile_url = event['profile_url']
        
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'room_name': room_name,
            'profile_url': profile_url,
        }))
        
        
    @sync_to_async   
    def save_the_message(self, username, message, room):
        sender = get_user_model().objects.get(username=username)
        room = Room.objects.get(name=room)
        Messages.objects.create(
            sender = sender,
            content = message,
            room = room
        )
        