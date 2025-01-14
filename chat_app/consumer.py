from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from .models import ChatMessage
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope["url_route"]["kwargs"]["username"]
        self.user_group_name = f"user_{self.username}"

        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender_username = text_data_json["sender"]
        recipient_username = text_data_json["recipient"]

        sender = await sync_to_async(User.objects.get)(username=sender_username)
        recipient = await sync_to_async(User.objects.get)(username=recipient_username)

        await sync_to_async(ChatMessage.objects.create)(
            user=sender,
            recipient=recipient,
            message=message,
        )

        await self.channel_layer.group_send(
            f"user_{recipient_username}",
            {
                "type": "chat_message",
                "message": message,
                "sender": sender_username,
            }
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps({
                "message": event["message"],
                "sender": event["sender"],
            })
        )
