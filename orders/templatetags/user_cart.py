from django import template
from django.contrib.auth import get_user_model

from orders.models import Order

register = template.Library()
User = get_user_model()


@register.simple_tag
def cart_quantity(request, *args, **kwargs):

    cart = Order.objects.filter(buyer__id=request.user.id).first()
    if cart:
        return cart.total_items
    return '0'
