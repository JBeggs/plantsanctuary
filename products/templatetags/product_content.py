from django import template
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.middleware.csrf import get_token
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from djangocms_blog.models import Post, BlogCategory

from api.models import Content, BlogContent
from products.models import Product, ProductCategory

register = template.Library()
User = get_user_model()


@register.simple_tag
def get_product_list_latest(request, *args, **kwargs):

    products = Product.objects.all().order_by('-id')[:10]

    html = ''

    for product in products:
        html += '<div class="single-best-seller-product d-flex align-items-center">'
        html += '<div class="product-thumbnail">'
        html += f'  <a href="/product/{product.id}">' \
                f'      <img src="/media/{product.image}" alt="{product.desc}" title="{product.desc}">' \
                f'  </a>' \
                f'</div>'
        html += '<div class="product-info">'
        html += f'  <a href="/product/{product.id}">{product.name}</a>' \
                f'  <p>{product.desc}</p>' \
                f'  <p>R {product.price}</p>' \
                f'</div>'
        html += '</div>'
    return mark_safe(html)


@register.simple_tag
def get_category_search_products():
    categories = ProductCategory.objects.filter()

    html = f''
    for cat in categories:
        number_products = Product.objects.filter(category=cat)
        html += f'<div class="custom-control custom-checkbox d-flex align-items-center mb-2">'
        html += f'<input type="checkbox" class="custom-control-input" id="id_{slugify(cat.name)}">'
        html += f'<label class="custom-control-label" for="id_{slugify(cat.name)}">{cat.name}<span class="text-muted">({number_products.count()})</span></label>'
        html += f'</div>'
    return mark_safe(html)
