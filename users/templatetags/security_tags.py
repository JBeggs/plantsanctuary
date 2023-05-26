from django import template
from django.contrib.auth import get_user_model

register = template.Library()
User = get_user_model()


@register.simple_tag
def site_manager(type, *args, **kwargs):

    manager = User.objects.filter(first_name='Wikus').first()
    if manager:
        if type == 'email':
            return manager.email
        if type == 'phone':
            if manager.phone:
                return manager.phone.phone_number
    return ''
