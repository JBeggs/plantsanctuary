from cms.app_base import CMSApp
from cms.models import Page
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from os.path import exists
from django.conf import settings
from plantsanctuary.api.models import *


def site_server(request, *args, **kwargs):

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
