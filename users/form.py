# import form class from django
from django import forms

# import GeeksModel from models.py
from .models import User, PhoneNumber, Profile, Address


# create a ModelForm
class UserForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = User
        exclude = ('username', 'password', 'last_login', 'is_superuser', 'groups', 'user_permissions', 'is_staff', 'date_joined')


class PhoneNumberForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = PhoneNumber
        exclude = ('user', 'security_code', 'is_verified', 'sent',)


class ProfileForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Profile
        exclude = ('user',)


class AddressForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Address
        exclude = ('user',)