from django.contrib import admin
from django.urls import include, path
from api.views import build, build_html, site_server

admin.autodiscover()

urlpatterns = [
    path(r'build',      build, name='build'),
    path(r'build_html', build_html, name='build_html'),
    path(r'site_server', site_server, name='site_server'),
]
