from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from rest_framework import viewsets

from products.models import Product
from users.models import Address
from .models import Order, OrderItem
from .permissions import (
    IsOrderByBuyerOrAdmin,
    IsOrderItemByBuyerOrAdmin,
    IsOrderItemPending,
    IsOrderPending
)
from .serializers import OrderItemSerializer, OrderReadSerializer, OrderWriteSerializer
from django.views.generic.edit import FormView
from .forms import OrderForm


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    CRUD order items that are associated with the current order id.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsOrderItemByBuyerOrAdmin]

    def get_queryset(self):
        res = super().get_queryset()
        order_id = self.kwargs.get('order_id')
        return res.filter(order__id=order_id)

    def perform_create(self, serializer):
        order = get_object_or_404(Order, id=self.kwargs.get('order_id'))
        serializer.save(order=order)

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            self.permission_classes += [IsOrderItemPending]

        return super().get_permissions()


class OrderViewSet(viewsets.ModelViewSet):
    """
    CRUD orders of a user
    """
    queryset = Order.objects.all()
    permission_classes = [IsOrderByBuyerOrAdmin]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return OrderWriteSerializer

        return OrderReadSerializer

    def get_queryset(self):
        res = super().get_queryset()
        user = self.request.user
        return res.filter(buyer=user)

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes += [IsOrderPending]

        return super().get_permissions()


class OrderFormView(FormView):

    template_name = "orders.html"
    form_class = OrderForm
    success_url = "/thanks/"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)


class OrdersView(TemplateView):

    template_name = 'orders.html'

    def post(self, request, *args, **kwargs):

        post_data        = request.POST or None

        order = Order.objects.filter(buyer=request.user).first()

        if not order:

            order = Order()
            order.buyer = request.user

            billng_address = Address.objects.filter(user=request.user,address_type='B', default=True).first()
            shipping_address = Address.objects.filter(user=request.user, address_type='S', default=True).first()
            if billng_address:
                order.billing_address = billng_address
            if shipping_address:
                order.shipping_address = shipping_address

            if billng_address and shipping_address:
                order.save()
            else:
                messages.success(self.request, "Please and Billing and shipping addresses.")
                return redirect(request.META.get('HTTP_REFERER'))

        if 'product_pk' in request.POST:
            order_item = OrderItem()
            order_item.order = order
            order_item.product_id = request.POST['product_pk']
            order_item.quantity = 1
            order_item.save()
            return redirect(request.META.get('HTTP_REFERER'))

        return self.render_to_response({'order': order, 'order_items':OrderItem.objects.filter(order_id=order.id)})

    def get(self, request, *args, **kwargs):

        return self.post(request, *args, **kwargs)
