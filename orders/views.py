from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
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


@method_decorator(csrf_exempt, name='dispatch')
class OrdersView(TemplateView):

    template_name = 'orders.html'

    def post(self, request, *args, **kwargs):

        post_data        = request.POST or None

        if request.user.is_anonymous:
            messages.error(self.request, "Please register and login to add to the cart...")
            return redirect(request.META.get('HTTP_REFERER'))

        order = Order.objects.filter(Q(buyer=request.user) & Q(status='P')).first()
        confirmed_order = Order.objects.filter(Q(buyer=request.user) & Q(status='C')).first()
        if not order and not confirmed_order:

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

        if 'product_pk' in request.POST and not confirmed_order:
            order_item = OrderItem()
            order_item.order = order

            order_item_check = OrderItem.objects.filter(product_id=request.POST['product_pk']).first()
            if order_item_check:
                updated_quantity = order_item_check.quantity + int(request.POST['quantity'])
                if updated_quantity <= order_item_check.quantity:
                    order_item_check.quantity = order_item_check.quantity + int(request.POST['quantity'])
                    order_item_check.save()
                else:
                    messages.success(self.request, "Cannot place order, not enough stock...")
            else:
                order_item.product_id = request.POST['product_pk']
                order_item.quantity = request.POST['quantity']
                order_item.save()

        if confirmed_order:
            messages.success(self.request, "There is a confirmed order in proccessing, please be patient...")
        return redirect(request.META.get('HTTP_REFERER'))

        # return self.render_to_response({'order': order, 'order_items':OrderItem.objects.filter(order_id=order.id)})

    def get(self, request, *args, **kwargs):

        return self.post(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class CartView(TemplateView):

    template_name = 'cart.html'

    def post(self, request, *args, **kwargs):

        if request.user.is_anonymous:
            messages.error(self.request, "Please register and login to add to the cart...")
            return redirect(request.META.get('HTTP_REFERER'))

        placed_order = Order.objects.filter(Q(buyer=request.user) & Q(status='C')).first()

        if not placed_order:

            order = Order.objects.filter(Q(buyer=request.user) & Q(status='P')).first()
            if not order:
                order = Order()
                order.buyer = request.user

                billng_address = Address.objects.filter(user=request.user, address_type='B', default=True).first()
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

            address = Address.objects.filter(
                Q(user_id=order.buyer.id) &
                Q(address_type='S')
            ).first()
            order_items = OrderItem.objects.filter(order_id=order.id)
        else:
            order = placed_order
            address = Address.objects.filter(
                Q(user_id=placed_order.buyer.id) &
                Q(address_type='S')
            ).first()
            order_items = OrderItem.objects.filter(order_id=placed_order.id)

        return self.render_to_response({
            'placed_order': placed_order,
            'order': order,
            'order_items': order_items,
            'address': address,
        })

    def get(self, request, *args, **kwargs):

        return self.post(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class OrderView(TemplateView):

    template_name = 'order_admin.html'

    def post(self, request, *args, **kwargs):

        if request.user.is_anonymous:
            messages.error(self.request, "Please register and login...")
            return redirect(request.META.get('HTTP_REFERER'))

        order = Order.objects.filter(id=kwargs['order_id']).first()
        address = Address.objects.filter(
            Q(user_id=order.buyer.id) &
            Q(address_type='S')
        ).first()
        order_items = OrderItem.objects.filter(order_id=order.id)

        return self.render_to_response({
            'order': order,
            'order_items': order_items,
            'address': address,
        })

    def get(self, request, *args, **kwargs):

        return self.post(request, *args, **kwargs)


def update_cart_item(request, item_id):

    if item_id:
        update = OrderItem.objects.filter(pk=item_id).first()
        if request.user == update.order.buyer or request.user.is_staff:
            update.quantity = int(request.POST['quantity'])
            update.save()

    return redirect(request.META.get('HTTP_REFERER'))


def delete_cart_item(request, item_id):

    if item_id:
        delete = OrderItem.objects.filter(pk=item_id).first()
        if request.user == delete.order.buyer or request.user.is_staff:
            delete.delete()

    return redirect(request.META.get('HTTP_REFERER'))


def place_order(request):

    order = Order.objects.filter(buyer=request.user).first()
    if request.user == order.buyer:
        items = OrderItem.objects.filter(order_id=order.id)
        can_process = True
        for item in items:
            product = Product.objects.get(id=item.product.id)
            if item.quantity > product.quantity:
                can_process = False
                messages.success(request, f"Item {item.product.name} cannot place order, to few items...")
                break

        if can_process:
            for item in items:
                product = Product.objects.get(id=item.product.id)
                product.quantity = product.quantity - item.quantity
                product.save()
            order.status = 'C'
            order.save()
            messages.success(request, "Order has been placed...")
    else:
        messages.success(request, "There was an error, not your order...")

    return redirect(request.META.get('HTTP_REFERER'))
