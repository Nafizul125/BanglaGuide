import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if text_data is None:
            return
        data = json.loads(text_data)
        message = data.get('message')
        user = self.scope.get('user')
        username = getattr(user, 'username', None) or getattr(user, 'name', '')
        if not username and isinstance(user, AnonymousUser):
            username = 'Anonymous'
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat.message',
                'message': message,
                'user': username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({'message': event['message'], 'user': event['user']}))