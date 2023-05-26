from django.contrib import admin

from .models import Content, BlogContent


class ContentAdmin(admin.ModelAdmin):
    list_display = ("creator", "name", "short_description",  "image_tag", 'created_at',)


class BlogContentAdmin(admin.ModelAdmin):
    list_display = ("author", "blog", "name", "short_description", "image_tag", 'created_at',)


admin.site.register(Content, ContentAdmin)
admin.site.register(BlogContent, BlogContentAdmin)
