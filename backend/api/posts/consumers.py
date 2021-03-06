import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from . import settings
from . import models


class AdminPostConsumer(AsyncWebsocketConsumer):
    async def send_json(self, data):
        await self.send(json.dumps(data))

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

    async def receive(self, text_data):
        try:
            json_data = json.loads(text_data)

        except ValueError:
            # Ignore malformed data
            print("Malformed JSON data received")
            return

        if not isinstance(json_data, dict):
            return

        request_type = json_data.get("type", None)
        if request_type is None:
            return

        if request_type == "approval":
            post_id = json_data.get("post_id", None)
            status = json_data.get("status", None)

            if post_id and status:
                await self.approve_post(post_id, status)
        elif request_type == "all_posts":
            await self.request_posts()

    async def disconnect(self, close_code):
        if self.group_name is not None:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    def get_posts(self):
        return models.Post.objects.all()

    async def request_posts(self):
        """Request for all the posts"""
        posts = await database_sync_to_async(self.get_posts)()
        for post in posts:
            await self.send_json(models.post_to_dict(post))

    def get_post(self, post_id):
        return models.Post.objects.get(pk=post_id)

    async def new_post(self, event):
        """Handler for new post"""
        data = event["text"]
        post = await database_sync_to_async(self.get_post)(data["id"])
        await self.send_json(models.post_to_dict(post))

    def update_post(self, post_id, status):
        post = models.Post.objects.get(pk=post_id)
        if status == settings.STATUS_APPROVED:
            post.isApproved = True
        elif status == settings.STATUS_REJECTED:
            post.isApproved = False

        post.save()
        return post

    async def approve_post(self, post_id, status):
        """Handler for approving posts"""
        post = await database_sync_to_async(self.update_post)(post_id, status)

        # Send to PostConsumer Group if it is an approved post
        if status == settings.STATUS_APPROVED:
            await self.channel_layer.group_send(
                settings.POSTS_GROUP_NAME,
                {
                    "type": "new_post",
                    "text": {"id": post.pk}
                }
            )


class PostConsumer(AsyncWebsocketConsumer):
    async def send_json(self, data):
        await self.send(json.dumps(data))

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
        try:
            json_data = json.loads(text_data)
        except ValueError:
            print("Malformed JSON data received")
            return

        if not isinstance(json_data, dict):
            return

        request_type = json_data.get("type", None)
        if request_type is None:
            return

        if request_type == "all_posts":
            await self.request_posts()

    def get_posts(self):
        return models.Post.objects.filter(isApproved=True)

    async def request_posts(self):
        """Request for all the approved posts"""
        posts = await database_sync_to_async(self.get_posts)()
        for post in posts:
            await self.send_json(models.post_to_dict(post))

    def get_post(self, post_id):
        return models.Post.objects.get(pk=post_id)

    async def new_post(self, event):
        data = event["text"]
        post = await database_sync_to_async(self.get_post)(data["id"])
        await self.send_json(models.post_to_dict(post))
