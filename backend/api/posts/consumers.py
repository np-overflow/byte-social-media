import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from . import settings
from . import models


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

    def get_posts(self):
        return models.Post.objects.all()

    async def request_posts(self, event):
        """Request for all the posts"""
        self.posts = await database_sync_to_async(self.get_posts)()
        for post in self.posts:
            await self.send_json(models.post_to_dict(post))

    async def new_post(self, event):
        """Handler for new post"""
        self.posts.append(event["post"])
        await self.send_json(models.post_to_dict(event["post"]))


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
