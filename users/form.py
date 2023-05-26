# import form class from django
from django import forms

# import GeeksModel from models.py
from .models import User, PhoneNumber, Profile, Address
from django.core.validators import validate_email


# create a ModelForm
class UserForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = User
        exclude = ('username', 'password', 'last_login', 'is_superuser', 'groups', 'user_permissions', 'is_staff', 'date_joined')

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #
    #     try:
    #         validate_email(email)
    #         return email
    #     except:
    #         self.add_error('email', 'Invalid email address')
    #
    #     return email

class PhoneNumberForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = PhoneNumber
        exclude = ('user', 'security_code', 'is_verified', 'sent',)

    def __init__(self, *args, **kwargs):
        super(PhoneNumberForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name == 'default':
                visible.field.widget.attrs['class'] = 'custom-control-input'
            else:
                visible.field.widget.attrs['class'] = 'form-control'


class ProfileForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Profile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AddressForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Address
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name == 'default':
                visible.field.widget.attrs['class'] = 'custom-control-input'
            else:
                visible.field.widget.attrs['class'] = 'form-control'
