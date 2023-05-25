from cms.app_base import CMSApp
from cms.models import Page
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from os.path import exists
from django.conf import settings

from api.models import Content, BlogContent
from products.models import *


def site_server(request, *args, **kwargs):

    site    = request.GET.get('site')
    section = request.GET.get('section')
    element = request.GET.get('element')
    product = request.GET.get('product', '')

    if section == 'main' and not element:
        default_layout = 'includes/main.html'
    elif section == 'main':
        default_layout = 'layouts/main/{}.html'.format(element)
    else:
        default_layout = 'layouts/{}/{}.html'.format(section, element)

    if product != '':
        products = Product.objects.filter(id=product)
    else:
        products = Product.objects.filter(quantity__gt=0)

    site_layout = 'layouts/{}/{}-{}.html'.format(section, site, element)

    try:
        from django.template.loader import get_template
        get_template(site_layout)
        site_template = site_layout
    except:
        site_template = default_layout

    return render(request, site_template, {'products': products, 'site': site})


@login_required
def build(request):
    site = request.GET.get('site')

    if request.POST.get('content'):
        site    = request.GET.get('site')
        section = request.GET.get('section')
        element = request.GET.get('element')
        layout  = '{}/contentserver/templates/layouts/{}/{}-{}.html'.format(settings.BASE_DIR, section, site, element)
        with open(layout, "w") as file:
            file.write(request.POST.get('content'))
            file.close()

        try:
            from django.template.loader import get_template
            get_template('layouts/{}/{}-{}.html'.format(section, site, element))
        except:

            with open(layout, "w") as file:
                file.write(request.POST.get('content'))
                file.close()

    #return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'build.html', {'posts': 'posts', 'site': site})


@login_required
def build_html(request):

    site    = request.GET.get('site')
    section = request.GET.get('section')
    element = request.GET.get('element')

    if section == 'main' and not element:
        default_layout = 'includes/main.html'
    elif section == 'main':
        default_layout = 'layouts/main/{}.html'.format(element)
    else:
        default_layout = 'layouts/{}/{}.html'.format(section, element)

    site_layout = 'layouts/{}/{}-{}.html'.format(section, site, element)

    try:
        from django.template.loader import get_template
        get_template(site_layout)
        site_template = site_layout
    except:
        site_template = default_layout

    return render(request, site_template, {'posts': 'posts', 'site': site})


@login_required
def update_content(request):

    if request.POST:

        image = {
            key: value for key, value in request.POST.items()
            if 'textarea_editor_'.lower() in key.lower()
        }
        name = {
            key: value for key, value in request.POST.items()
            if 'image_content_editor_'.lower() in key.lower()
        }
        desc = ''
        if bool(image):
            desc = image[next(iter(image))]

        if bool(name):
            name = next(iter(name)).replace('image_content_editor_', '')
        else:
            name = next(iter(image)).replace('textarea_editor_', '')

        content = Content.objects.filter(name=name).first()

        for key, in_memory_file in request.FILES.items():
            content.image = in_memory_file

        content.desc = desc
        if request.user.is_staff:
            content.save()

    else:
        partial_key = 'textarea_editor_'

        matching_items = {
            key: value for key, value in request.GET.items()
            if partial_key.lower() in key.lower()
        }

        for element, content in matching_items.items():
            name = element.replace(partial_key, "")
            element_content = Content.objects.filter(name=name).first()
            element_content.desc = content
            if request.user.is_staff:
                element_content.save()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def update_blog_content(request):

    if request.POST:
        blog_id = request.GET.get('blog_id', None)
        image = {
            key: value for key, value in request.POST.items()
            if 'textarea_editor_'.lower() in key.lower()
        }
        name = {
            key: value for key, value in request.POST.items()
            if 'image_content_editor_'.lower() in key.lower()
        }
        desc = ''
        if bool(image):
            desc = image[next(iter(image))]

        if bool(name):
            name = next(iter(name)).replace('image_content_editor_', '')
        else:
            name = next(iter(image)).replace('textarea_editor_', '')

        content = BlogContent.objects.filter(
            Q(name=name) &
            Q(blog_id=blog_id)
        ).first()

        for key, in_memory_file in request.FILES.items():
            content.image = in_memory_file

        content.desc = desc
        if request.user == content.author:
            content.save()

    else:

        blog_id = request.GET.get('blog_id', None)
        partial_key = 'textarea_editor_'

        matching_items = {
            key: value for key, value in request.GET.items()
            if partial_key.lower() in key.lower()
        }

        for element, content in matching_items.items():
            name = element.replace(partial_key, "")
            element_content = BlogContent.objects.filter(
                Q(name=name) &
                Q(blog_id=blog_id)
            ).first()
            element_content.desc = content
            if request.user == element_content.author:
                element_content.save()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def delete(request, content_id):

    if id:
        delete = Content.objects.filter(pk=content_id).first()
        if request.user == delete.author:
            delete.delete()

    return redirect(request.META.get('HTTP_REFERER'))
