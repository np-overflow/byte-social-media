from django.db import models


class Post(models.Model):
    post_id = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    date = models.DateTimeField()
    author = models.CharField(max_length=100)
    caption = models.CharField(max_length=400)
    kind = models.CharField(max_length=10)
    # Fixed Length should be 32 + 4 (4 for extension)
    src = models.CharField(max_length=36)
    isApproved = models.BooleanField(null=True)


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
