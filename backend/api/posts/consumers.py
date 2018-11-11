import json

from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from django.apps import apps

from . import settings


class AdminPostConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = None
        # Only allow superusers
        if self.scope["user"].is_superuser:
            self.group_name = settings.ADMIN_GROUP_NAME

            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )

            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.group_name is not None:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )


class PostConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = settings.POSTS_GROUP_NAME

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        await self.send(text_data=text_data)

    async def new_post(self, event):
        await self.send(text_data=json.dumps(event["text"]))
