from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from django.apps import apps

from . import settings


class PostConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = settings.POSTS_GROUP_NAME

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        pass

    async def receive(self, text_data):
        await self.send(text_data=text_data)