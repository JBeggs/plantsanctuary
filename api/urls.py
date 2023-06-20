from django.contrib import admin
from django.urls import include, path
from .views import build, build_html, site_server, update_content, update_blog_content, delete_content, delete_product, delete_blog, update_product_content

admin.autodiscover()

urlpatterns = [
    path(r'build',      build, name='build'),
    path(r'build_html', build_html, name='build_html'),
    path(r'site_server', site_server, name='site_server'),
    path(r'update_content',     update_content, name='update_content'),
    path(r'update_blog_content', update_blog_content, name='update_blog_content'),
    path(r'update_product_content', update_product_content, name='update_product_content'),
    path(r'delete_content/<_id>/',     delete_content, name='delete_content'),
    path(r'delete_product/<_id>/', delete_product, name='delete_product'),
    path(r'delete_blog/<_id>/', delete_blog, name='delete_blog'),
]
