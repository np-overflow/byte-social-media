from django.db.models.signals import post_save
from django.dispatch import receiver

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from . import models
from . import settings

channel_layer = get_channel_layer()


@receiver(post_save, sender=models.Post)
def update_socket_group(sender, instance, **kwargs):
    async_to_sync(channel_layer.group_send)(
        settings.POSTS_GROUP_NAME,
        {
            "type": "new_post",
            "text": models.post_to_dict(instance),
        }
    )
