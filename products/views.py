from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework import permissions, viewsets

from orders.models import Order, OrderItem
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

        categories = request.GET.get("categories", '')
        sort = request.GET.get("sort", '')
        products = Product.objects.filter(Q(active=True) & Q(quantity__gt=0))
        if categories:
            categories = categories.split(',')
            q = Q()
            for cat in categories:
                if cat:
                    q = q | Q(category__name__icontains=cat)
            products = products.filter(q)

        if sort:
            sort = sort.replace(',', '')
            if sort == 'new_arrivals':
                products = products.order_by('-id')
            elif sort == 'a_z':
                products = products.order_by('name')
            elif sort == 'z_a':
                products = products.order_by('-name')
            elif sort == 'low_high':
                products = products.order_by('price')
            elif sort == 'high_low':
                products = products.order_by('-price')
        show = request.GET.get("show", 9)
        paginator = Paginator(products, int(show))  # Show 25 contacts per page.
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        orders = Order.objects.filter(status='C')
        return self.render_to_response({
            'orders': orders,
            'products': products,
            'page_obj': page_obj,
            'paginator': paginator,
            'add_product': add_product
        })

    def get(self, request, *args, **kwargs):

        return self.post(request, *args, **kwargs)


class ProductView(TemplateView):

    template_name = 'product.html'
    form = ProductForm

    def post(self, request, *args, **kwargs):

        key = kwargs['slug'].replace('-', ' ').split()
        if len(key) > 2:
            key = kwargs['slug'].replace('-', ' ').split()[0] + ' ' \
                    '' + kwargs['slug'].replace('-', ' ').split()[1] + ' ' + kwargs['slug'].replace('-', ' ').split()[2]
        else:
            key = kwargs['slug'].replace('-', ' ').split()[0]

        product = Product.objects.filter(name__istartswith=key).first()

        return self.render_to_response({
            'product': product,
        })

    def get(self, request, *args, **kwargs):

        return self.post(request, *args, **kwargs)
