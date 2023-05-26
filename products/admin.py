from django.contrib import admin

from .models import Product, ProductCategory


class ProductAdmin(admin.ModelAdmin):
    list_display = ("seller", "name", "short_description",  "image_tag", 'created_at',)


admin.site.register(ProductCategory)
admin.site.register(Product, ProductAdmin)

