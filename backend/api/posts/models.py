from django.db import models


class Media(models.Model):
    kind = models.CharField(max_length=10)
    src = models.TextField()


class Post(models.Model):
    author = models.CharField(max_length=100)
    caption = models.CharField(max_length=400)
    isApproved = models.BooleanField(null=True)
    models.ForeignKey(Media, on_delete=models.PROTECT, null=True)
