from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import Message, User, Room


class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_pk = self.scope["url_route"]["kwargs"]["pk"]
        self.room_group_name = f"chat_{self.room_pk}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        await self.save_message_to_database(text_data_json)

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": text_data_json}
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

    
    @database_sync_to_async
    def save_message_to_database(self, text_data_json):
        message = text_data_json["message"]
        user_id = int(text_data_json["user"])
        room = self.room_pk

        user = User.objects.get(id=user_id)
        room = Room.objects.get(pk=room)

        Message.objects.create(
            body=message,
            user=user,
            room=room
        )
