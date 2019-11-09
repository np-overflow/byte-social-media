import django
import base64
import math
import os
import sys
from enum import Enum

# Django setup to allow interfacing with django models
def setup_django():
    # Add api to system path to facilitate importing of modules from it
    sys.path.append('/root/api')

    # Django setup to interface with api through django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
    django.setup()

setup_django()  # Must be run before importing models

from posts import models


class SocialPlatform(Enum):
    Facebook = "facebook"
    Instagram = "instagram"
    Twitter = "twitter"
    Telegram = "telegram"


class ContentType(Enum):
    Video = "video"
    Image = "image"


def create_media(kind, src):
    return {
        "kind": kind,
        "src": src,
    }


def create_post(post_id, platform, date, author, caption, media):
    if not models.Post.objects.filter(post_id=post_id, platform=platform).exists():
        return models.Post.objects.create(
            post_id=post_id, platform=platform, date=date,
            author=author, caption=caption, **media)
    else:
        return


def int_id_to_str(int_id):
    """Converts an integer ID to a string that can be used in the DB"""
    num_bytes = math.ceil(int_id.bit_length() / 8)
    int_bytes = int_id.to_bytes(num_bytes, "big")
    return base64.b64encode(int_bytes)
