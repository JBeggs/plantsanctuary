from django import template
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.middleware.csrf import get_token
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from api.models import Content, BlogContent
from orders.models import OrderItem
from products.models import Product, ProductCategory
from users.models import Address

register = template.Library()
User = get_user_model()


@register.simple_tag
def get_product_list_latest(request, *args, **kwargs):

    products = Product.objects.all().order_by('-id')[:10]

    html = ''

    for product in products:
        html += '<div class="single-best-seller-product d-flex align-items-center">'

        if product.thumbnail:
            image = product.thumbnail
        else:
            image = product.image

        html += '<div class="product-thumbnail">'
        html += f'  <a href="/product/{product.id}">' \
                f'      <img src="/media/{image}" alt="{product.desc}" title="{product.desc}">' \
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
        html += f'<div class="category custom-control custom-checkbox d-flex align-items-center mb-2">'
        html += f'<table style="width:100%;"><tr><td style="width:50%;">' \
                f'<input onchange="shop_filter();" type="checkbox" class="custom-control-input" id="id_{slugify(cat.name)}">'
        html += f'<label class="custom-control-label" for="id_{slugify(cat.name)}">{cat.name}' \
                f'</label></td><td style="width:50%;"><span class="text-muted">( {number_products.count()} )</span></td>'
        html += f'</tr></table></div>'
    return mark_safe(html)


@register.simple_tag
def get_order_items(request, order_id):
    order_items = OrderItem.objects.filter(order_id=order_id)

    html = '<table>'
    for item in order_items:
        html += f'<tr><td>{item.product.name}</td><td>{item.quantity}</td><td>{item.cost}</td></tr>'

    html += '</table>'
    return mark_safe(html)


@register.simple_tag
def get_address(user_id):

    address = Address.objects.filter(
        Q(user_id=user_id) &
        Q(address_type='S')
    ).first()

    return mark_safe(address.html())

