import datetime
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import NotAcceptable
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django_countries.fields import CountryField


User = get_user_model()


class PhoneNumber(models.Model):
    user = models.OneToOneField(
        User, related_name='phone', on_delete=models.CASCADE)
    phone_number = PhoneNumberField(unique=True)
    security_code = models.CharField(max_length=120)
    is_verified = models.BooleanField(default=False)
    sent = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_number.__str__()


class Profile(models.Model):
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatar', blank=True)
    bio = models.CharField(max_length=200, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.user.get_full_name()


class Address(models.Model):
    # Address options
    BILLING = 'B'
    SHIPPING = 'S'

    ADDRESS_CHOICES = ((BILLING, _('billing')), (SHIPPING, _('shipping')))
    PROVINCE_CHOICES = (
        ('------------', 'Please Select'),
        ('Western Cape', 'Western Cape'),
        ('Eastern Cape', 'Eastern Cape'),
        ('Northern Cape', 'Northern Cape'),
        ('North West', 'North West'),
        ('Free State', 'Free State'),
        ('Kwazulu Natal', 'Kwazulu Natal'),
        ('Gauteng', 'Gauteng'),
        ('Limpopo Mpumlanga', 'Limpopo Mpumlanga')
    )

    user = models.ForeignKey(
        User, related_name='addresses', on_delete=models.CASCADE)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    country = CountryField()
    city = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    province = models.CharField(max_length=28, choices=PROVINCE_CHOICES, default='------------')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.user.get_full_name()
