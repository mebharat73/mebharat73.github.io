# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Room
from django.contrib.auth.models import User

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
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        # Save the message to the database
        room = Room.objects.get(name=self.room_name)
        user = User.objects.get(username=username)  # Ensure you have the user object

        Message.objects.create(user=user, room=room, message=message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'profile_pic_url': user.profile.profile_pic.url if user.profile.profile_pic else None
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        profile_pic_url = event['profile_pic_url']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'profile_pic_url': profile_pic_url
        }))