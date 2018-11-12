from django.db import models


class Media(models.Model):
    kind = models.CharField(max_length=10)
    src = models.TextField()


class Post(models.Model):
    author = models.CharField(max_length=100)
    platform = models.CharField(max_length=10)
    caption = models.CharField(max_length=400)
    isApproved = models.BooleanField(null=True)
    media = models.ForeignKey(Media, on_delete=models.PROTECT, null=True)


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
            "media": media_to_dict(post_instance.media),
        }