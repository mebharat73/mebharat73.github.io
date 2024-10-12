from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.contrib.auth.models import User
from .models import Message
import asyncio
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope['user'].is_authenticated:
            self.room_group_name = None
            await self.close()
        else:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'chat_%s' % self.room_name

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

    async def disconnect(self, close_code):
        if self.room_group_name is not None:
            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    

    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        # Create a new Message instance with the current user
        await asyncio.to_thread(self.save_message_to_database, message, username)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'profile_pic_url': await self.get_profile_pic_url(),  # Fix here
            }
        )

    def save_message_to_database(self, message, username):
        import django.db.transaction as transaction  # Import transaction here
        with transaction.atomic():
            user = User.objects.get(username=username)
            Message.objects.create(room=self.room_name, user=user, message=message)

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        profile_pic_url = event['profile_pic_url']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'profile_pic_url': profile_pic_url,
        }))

    def _get_profile_pic_url(self):
        return self.scope['user'].profile.profile_pic.url

    async def get_profile_pic_url(self):
        return await sync_to_async(self._get_profile_pic_url)()