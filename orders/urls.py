from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OrderItemViewSet, OrderViewSet


app_name = 'orders'

router = DefaultRouter()
router.register('^(?P<order_id>\d+)/order-items', OrderItemViewSet)
router.register('', OrderViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('list/', OrderViewSet.as_view(({'get': 'list'})))
]
