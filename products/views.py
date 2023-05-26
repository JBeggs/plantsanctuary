from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework import permissions, viewsets

from .forms import ProductForm
from .models import Product, ProductCategory
from .permissions import IsSellerOrAdmin
from .serializers import ProductCategoryReadSerializer, ProductReadSerializer, ProductWriteSerializer
from django.core.paginator import Paginator


class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and Retrieve product categories
    """
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryReadSerializer
    permission_classes = (permissions.AllowAny, )


class ProductViewSet(viewsets.ModelViewSet):
    """
    CRUD products
    """
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return ProductWriteSerializer

        return ProductReadSerializer

    def get_permissions(self):
        if self.action in ("create", ):
            self.permission_classes = (permissions.IsAuthenticated, )
        elif self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes = (IsSellerOrAdmin, )
        else:
            self.permission_classes = (permissions.AllowAny, )

        return super().get_permissions()


class ProductsView(TemplateView):

    template_name = 'products.html'
    form = ProductForm

    def post(self, request, *args, **kwargs):

        post_data = request.POST or None

        if post_data:
            add_product = self.form(post_data)
            product_form_valid = add_product.is_valid()
            if product_form_valid and 'image' in self.request.FILES:
                product = add_product.save(commit=False)
                product.image = self.request.FILES['image']
                product.save()
                messages.success(self.request, "{} saved successfully".format(product))
            else:
                add_product.add_error('image', 'Please add an image')

        else:
            add_product = self.form()

        products = Product.objects.filter(active=True)
        paginator = Paginator(products, 10)  # Show 25 contacts per page.
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return self.render_to_response({
            'products': products,
            'page_obj': page_obj,
            'paginator': paginator,
            'add_product': add_product
        })

    def get(self, request, *args, **kwargs):

        return self.post(request, *args, **kwargs)
