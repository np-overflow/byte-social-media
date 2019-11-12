import base64
import math
from enum import Enum
from django.db import models


class Post(models.Model):
    post_id = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=100)
    caption = models.CharField(max_length=400)
    kind = models.CharField(max_length=10)
    # Fixed Length should be 32 + 4 (4 for extension)
    src = models.CharField(max_length=36)
    isApproved = models.BooleanField(null=True)


class SocialPlatform(Enum):
    Facebook = "facebook"
    Instagram = "instagram"
    Twitter = "twitter"
    Telegram = "telegram"


class ContentType(Enum):
    Video = "video"
    Image = "image"


def int_id_to_str(int_id):
    """Converts an integer ID to a string that can be used in the DB"""
    num_bytes = math.ceil(int_id.bit_length() / 8)
    int_bytes = int_id.to_bytes(num_bytes, "big")
    return base64.b64encode(int_bytes)


def media_to_dict(media_instance):
    if media_instance is not None:
        return {
            "type": media_instance.kind,
            "src": media_instance.src,
        }


def post_to_dict(post_instance):
    if post_instance is not None:
        return {
            "id": post_instance.pk,
            "author": post_instance.author,
            "caption": post_instance.caption,
            "isApproved": post_instance.isApproved,
            "platform": post_instance.platform,
            "media": media_to_dict(post_instance),
        }
