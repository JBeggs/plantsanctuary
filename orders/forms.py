# import form class from django
from django import forms

# import GeeksModel from models.py
from .models import Order


# create a ModelForm
class OrderForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Order
        fields = "__all__"