import django
from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from orders.views import OrderFormView, OrdersView
from products.views import ProductsView
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

    path('products/', ProductsView.as_view(), name="products"),
    path('order/', OrderFormView.as_view(), name="order"),
    path('orders/', OrdersView.as_view(), name="ordera"),
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

