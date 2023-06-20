from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from djangocms_blog.models import Post

from products.models import Product

User = get_user_model()

from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image


def create_thumbnail(img, thumb, w, h):

    if not img:
        return

    image = Image.open(img.file).convert('RGB')
    # If the image is smaller than w x h, don't bother creating a thumbnail.
    width, height = image.size
    if width < w or height < h:
        return
    # Crop as little as possible to square, keeping the center.
    if width > height:
        delta = width - height
        left = int(delta / 2)
        upper = 0
        right = height + left
        lower = height
    else:
        delta = height - width
        left = 0
        upper = int(delta / 2)
        right = width
        lower = width + upper
    image = image.crop((left, upper, right, lower))
    # Create the thumbnail as a w x h square.
    image.thumbnail((w, h), Image.ANTIALIAS)
    # Save the thumbnail in the FileField.
    # Using Image.save(content, 'jpeg') seems to work for png too.
    buffer = BytesIO()
    image.save(buffer, 'jpeg', quality=95)
    cf = ContentFile(buffer.getvalue())
    thumb.save(name=img.name, content=cf, save=False)


def content_image_path(instance, filename):
    if '/' in filename:
        filename = filename.split('/')[-1]
    ext = filename.split('.')[-1]
    return f'content/images/{instance.name.replace(" ","")}/{instance.name.replace(" ","")}.{ext}'


def content_image_thumbnail_path(instance, filename):
    if '/' in filename:
        filename = filename.split('/')[-1]
    ext = filename.split('.')[-1]
    return f'content/thumb/{instance.name.replace(" ","")}/{instance.name.replace(" ","")}.{ext}'


class Content(models.Model):

    creator = models.ForeignKey(
        User, related_name="creator", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    desc = models.TextField(_('Description'), blank=True)
    image = models.ImageField(upload_to=content_image_path, blank=True, max_length=300)
    thumbnail = models.ImageField(upload_to=content_image_thumbnail_path, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active     = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.name

    def save(self):
        create_thumbnail(self.image, self.thumbnail, 400, 400)
        super(Content, self).save()

    def image_tag(self):
        from django.utils.html import escape
        try:
            return mark_safe(u'<img src="%s" />' % escape(self.thumbnail.url))
        except:
            try:
                return mark_safe(u'<img style="height:200px;" src="%s" />' % escape(self.image.url))
            except:
                return ''

    @property
    def short_description(self):
        return truncatechars(self.desc, 60)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


class BlogContent(models.Model):

    author = models.ForeignKey(
        User, related_name="author", on_delete=models.CASCADE)
    blog = models.ForeignKey(
        Post, related_name="blog", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    desc = models.TextField(_('Description'), blank=True)
    image = models.ImageField(upload_to=content_image_path, blank=True, max_length=500)
    thumbnail = models.ImageField(upload_to=content_image_thumbnail_path, blank=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active     = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.name

    def save(self):
        create_thumbnail(self.image, self.thumbnail, 400, 400)
        super(BlogContent, self).save()

    def image_tag(self):
        from django.utils.html import escape
        try:
            return mark_safe(u'<img src="%s" />' % escape(self.thumbnail.url))
        except:
            try:
                return mark_safe(u'<img style="height:200px;" src="%s" />' % escape(self.image.url))
            except:
                return ''

    @property
    def short_description(self):
        return truncatechars(self.desc, 60)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


class ProductContent(models.Model):

    creator = models.ForeignKey(
        User, related_name="product_creator", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    product = models.ForeignKey(
        Product, related_name="product", on_delete=models.CASCADE, blank=True, null=True)
    desc = models.TextField(_('Description'), blank=True)
    image = models.ImageField(upload_to=content_image_path, blank=True, max_length=300)
    thumbnail = models.ImageField(upload_to=content_image_thumbnail_path, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active     = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.name

    def save(self):
        create_thumbnail(self.image, self.thumbnail, 400, 400)
        super(ProductContent, self).save()

    def image_tag(self):
        from django.utils.html import escape
        try:
            return mark_safe(u'<img src="%s" />' % escape(self.thumbnail.url))
        except:
            try:
                return mark_safe(u'<img style="height:200px;" src="%s" />' % escape(self.image.url))
            except:
                return ''

    @property
    def short_description(self):
        return truncatechars(self.desc, 60)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
