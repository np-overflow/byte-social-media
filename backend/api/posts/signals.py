from django.db.models.signals import post_save
from django.dispatch import receiver

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from . import models
from . import settings

channel_layer = get_channel_layer()


def post_to_dict(post_instance):
    media = None
    if post_instance.media:
        media = {
            "type": post_instance.media.kind,
            "src": post_instance.media.src
        }

    return {
        "author": post_instance.author,
        "caption": post_instance.caption,
        "isApproved": post_instance.isApproved,
        "media": media
    }


@receiver(post_save, sender=models.Post)
def update_socket_group(sender, instance, **kwargs):
    async_to_sync(channel_layer.group_send)(
        settings.POSTS_GROUP_NAME,
        {
            "type": "new_post",
            "text": post_to_dict(instance),
        }
    )
