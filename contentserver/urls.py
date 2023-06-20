import django
from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from api.views import SearchView
from orders.views import OrderFormView, OrdersView, CartView, delete_cart_item, update_cart_item, place_order, OrderView
from products.views import ProductsView, ProductView
from users.views import UserView

admin.autodiscover()

urlpatterns = [
    path("sitemap.xml", sitemap, {"sitemaps": {"cmspages": CMSSitemap}}),
    path('api/user/', include('users.urls', namespace='users')),
    path('api/products/', include('products.urls', namespace='products')),
    path('api/user/orders/',
         include('orders.urls', namespace='orders')),
    path('api/user/payments/',
         include('payment.urls', namespace='payment')),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls'))
]

urlpatterns += (
    path('search/', SearchView.as_view(), name="search"),
    path('shop/', ProductsView.as_view(), name="shop"),
    path('shop/item/<slug>/', ProductView.as_view(), name="product-view"),
    path('cart/', CartView.as_view(), name="cart"),
    path('cart/delete/item/<item_id>/', delete_cart_item, name="delete_cart_item"),
    path('cart/update/item/<item_id>/', update_cart_item, name="update_cart_item"),
    path('order/', OrderFormView.as_view(), name="order"),
    path('order/place/', place_order, name="place_order"),
    path('orders/', OrdersView.as_view(), name="orders"),
    path('view/order/<order_id>/', OrderView.as_view(), name="order_view"),
    path('user/', UserView.as_view(), name="user"),
    path('accounts/', include('allauth.urls')),
    path("admin/", admin.site.urls),
    path("", include("cms.urls")),
    path('taggit_autosuggest/', include('taggit_autosuggest.urls')),
)

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

