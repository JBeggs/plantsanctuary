from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import truncatechars
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


User = get_user_model()


def category_image_path(instance, filename):
    if '/' in filename:
        filename = filename.split('/')[-1]
    return f'product/category/icons/{instance.name.replace(" ","")}/{filename}'


def product_image_path(instance, filename):
    if '/' in filename:
        filename = filename.split('/')[-1]
    return f'product/images/{instance.name.replace(" ","")}/{filename}'


def product_image_thumb_path(instance, filename):
    if '/' in filename:
        filename = filename.split('/')[-1]
    return f'product/thumb/{instance.name.replace(" ","")}/{filename}'


class ProductCategory(models.Model):
    name = models.CharField(_('Category name'), max_length=100)
    icon = models.ImageField(upload_to=category_image_path, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        verbose_name = _('Product Category')
        verbose_name_plural = _('Product Categories')

    def __str__(self):
        return self.name


def get_default_product_category():
    return ProductCategory.objects.get_or_create(name='Others')[0]


class Product(models.Model):
    seller = models.ForeignKey(
        User, related_name="products", on_delete=models.CASCADE)
    category = models.ForeignKey(
        ProductCategory, related_name="product_list", on_delete=models.SET(get_default_product_category))
    name = models.CharField(max_length=200)
    desc = models.TextField(_('Description'), blank=True)
    image = models.ImageField(upload_to=product_image_path, blank=True, max_length=300)
    thumbnail = models.ImageField(upload_to=product_image_thumb_path, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField(default=1)
    barcode = models.CharField(max_length=200, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active     = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.name

    def save(self):
        from api.models import create_thumbnail
        create_thumbnail(self.image, self.thumbnail, 200, 200)
        super(Product, self).save()

    @property
    def short_description(self):
        return truncatechars(self.desc, 60)

    def image_tag(self):
        from django.utils.html import escape
        try:
            return mark_safe(u'<img src="%s" />' % escape(self.thumbnail.url))
        except:
            try:
                return mark_safe(u'<img style="height:200px;" src="%s" />' % escape(self.image.url))
            except:
                return ''
