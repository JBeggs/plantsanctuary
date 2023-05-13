from django.contrib import admin
from django.urls import include, path
from .views import build, build_html, site_server, update

admin.autodiscover()

urlpatterns = [
    path(r'build',      build, name='build'),
    path(r'build_html', build_html, name='build_html'),
    path(r'site_server', site_server, name='site_server'),
    path(r'update',     update, name='update'),
]
