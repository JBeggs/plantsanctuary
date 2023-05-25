from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _
from djangocms_blog.models import Post

User = get_user_model()


def content_image_path(instance, filename):
    return f'content/images/{instance.name}/{filename}'


class Content(models.Model):

    creator = models.ForeignKey(
        User, related_name="creator", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    desc = models.TextField(_('Description'), blank=True)
    image = models.ImageField(upload_to=content_image_path, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active     = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.name


class BlogContent(models.Model):

    author = models.ForeignKey(
        User, related_name="author", on_delete=models.CASCADE)
    blog = models.ForeignKey(
        Post, related_name="blog", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    desc = models.TextField(_('Description'), blank=True)
    image = models.ImageField(upload_to=content_image_path, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active     = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.name
