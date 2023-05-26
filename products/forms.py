from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = Product
        fields = '__all__'
