from django import template
from django.contrib.auth import get_user_model
from django.db.models import Q, QuerySet
from django.middleware.csrf import get_token
from django.utils.safestring import mark_safe

from django.utils.text import slugify
#from djangocms_blog.models import BlogCategory, Post

from api.models import Content, BlogContent, ProductContent
from django.core.paginator import Paginator

from orders.models import Order
from products.models import Product

register = template.Library()
User = get_user_model()


def get_textarea(name, content):
    editor_width = len(content.desc)
    description = content.desc
    if '<img' in description:
        description = ''
    textarea = f'<textarea ' \
               f'style="min-width: 100%;" class="" ' \
               f'rows="6" cols="20" size="{editor_width}" type="text" ' \
               f'name="textarea_editor_{name}" id="id_textarea_editor__{name}">{description}' \
               f'</textarea>' \
               f''
    return textarea


def get_edit_textarea(name, content, form_action, _id):

    blog_input = f'<input type="hidden" name="id" value="{_id}">'
    image_style = 'style="width:10px;height:10px;background-color:white;"'
    edit_image = f'<img src="/media/img/edit.png" {image_style} />'
    edit_html = f"""{content.desc}<div style="" onclick='edit_data_{name}();' class='content_text_{name}'>
    {edit_image}</div>
    <script>
        function edit_data_{name}(){{  
            $("#myModal").modal("show");
            $(".modal-body").html($('.content_editor_{name}_div').html());
        }}
    </script>
    <div class="content_editor_{name}_div" style="display:none;">
    <form action="/api/{form_action}" method="get">
        {blog_input}
        {get_textarea(name, content)}
        <button class="btn alazea-btn" type="submit">Save</button>
    </form>
    </div>"""
    return mark_safe(edit_html.replace("{{", "{").replace("}}", "}"))


def get_edit_image(request, name, default_text, content, form_action, _type, _id):
    token = get_token(request)
    blog_input = f'<input type="hidden" name="id" value="{_id}">'
    content_type = content.__class__.__name__.replace('Content', '').lower()
    image_class = ''
    if 'class' in default_text:
        image_class = default_text.split('class=')[1].split('"')[1]
    image = False
    if _type == 'image':
        if content.image:
            image = f'<img src="/media/{content.image}"  />'

    elif _type == 'thumb':
        if content.thumbnail:
            image = f'<img src="/media/{content.thumbnail}"  />'

    if not image:
        image = f'{content.desc}'

    edit_image = '<img src="/media/img/edit.png" style="width:10px;height:10px;position:relative;background-color:white;" />'
    edit_html = f"""{image}<div onclick='edit_data_{name}();' class='content_text_{name}'>{edit_image}</div>
    <script>

        function edit_data_{name}(){{  
            $("#myModal").modal("show");
            $(".modal-body").html($('.content_editor_{name}_div').html());

        }}

    </script>
    <div class="content_editor_{name}_div" style="display:none;postition:relative;">
    <form class="content_editor_{name}" action="/api/{form_action}" method="post" enctype="multipart/form-data">
      <input type="file" id="image_content_editor_{name}" name="image_content_editor_{name}" accept="image/*">
      <input type="hidden" name="csrfmiddlewaretoken" value="{token}">
      {blog_input}
      {get_textarea(name, content)}
      <p>
      <input type="submit" class="btn alazea-btn">
      <input onclick="window.location='/api/delete_{content_type}/{content.id}/'" type="button" class="btn alazea-btn" value="Delete"></p>
    </form>
    </div>"""
    return mark_safe(edit_html.replace("{{", "{").replace("}}", "}"))


@register.simple_tag
def get_edit_content(request, name, _type, default_text, *args, **kwargs):
    editor = request.user
    content = Content.objects.filter(name=name).first()

    if not content and request.user.is_staff:
        content = Content()
        content.creator = request.user
        content.name = name
        content.desc = default_text
        content.save()

    if editor.is_staff:

        name = name.strip()

        if _type == 'desc':
            return get_edit_textarea(name, content, 'update_content', _id=None)
        if _type in ['image', 'thumb']:
            return get_edit_image(request, name, default_text, content, 'update_content', _type, _id=None)

    if not content:
        return ''
    if _type == 'url':
        if content.image:
            url = content.image
        else:
            url = content.desc
        return url
    if _type == 'desc':
        return mark_safe(content.desc)
    image = False
    if _type == 'image':
        if content.image:
            image = f'<img src="/media/{content.image}"  />'
    elif _type == 'thumb':
        if content.thumbnail:
            image = f'<img src="/media/{content.thumbnail}"  />'
    if not image:
        image = content.desc
    return mark_safe(image)


@register.simple_tag
def get_edit_content_button(request, name, _type, default_text, *args, **kwargs):
    editor = request.user
    content = Content.objects.filter(name=name).first()

    if not content and request.user.is_staff:
        content = Content()
        content.creator = request.user
        content.name = name
        content.desc = default_text
        content.save()

    if editor.is_staff:

        name = name.strip()
        editor_width = len(content.desc)

        if _type == 'desc':
            input = f'<input size="{editor_width}" type="text" name="editor_{name}" id="editor_{name}" value="{content.desc}" />'
            edit_html = f"""<div onclick='edit_data_{name}();' class='content_text_{name}'>{content.desc}</div>
            <script>
                function edit_data_{name}(){{  
                    $("#myModal").modal("show");
                    $(".modal-body").html($('.content_editor_{name}_div').html());
                }}
            </script>
            <div class="content_editor_{name}_div" style="display:none;">
            <form action="/api/update_content" method="get">
                {input}
            </form>
            </div>"""
            return mark_safe(edit_html.replace("{{", "{").replace("}}", "}"))

    if not content:
        return ''

    if _type == 'desc':
        return mark_safe(content.desc)


@register.simple_tag
def get_edit_content_blog(request, blog_id, name, _type, default_text, *args, **kwargs):

    editor = request.user
    content = BlogContent.objects.filter(
        Q(name=name) &
        Q(blog_id=blog_id)
    ).first()
    post = Post.objects.get(id=blog_id)
    if not content and request.user.is_staff:

        if request.user == post.author:
            content = BlogContent()
            content.author = request.user
            content.blog = post
            content.name = name
            content.desc = default_text
            content.save()

    if editor.is_staff and request.user == post.author:

        if _type == 'desc':
            return get_edit_textarea(name, content, 'update_blog_content', _id=blog_id)
        if _type in ['image', 'thumb']:
            return get_edit_image(request, name, default_text, content, 'update_content', _type, _id=blog_id)

    if not content:
        return ''

    if _type == 'desc':
        return mark_safe(content.desc)
    if _type == 'url':
        if content.image:
            url = content.image
        else:
            url = content.desc
        return url
    image = False
    if _type == 'image':
        if content.image:
            image = f'<img src="/media/{content.image}"  />'
    elif _type == 'thumb':
        if content.thumbnail:
            image = f'<img src="/media/{content.thumbnail}"  />'
    if not image:
        image = content.desc
    return mark_safe(image)


@register.simple_tag
def get_edit_content_product(request, product_id, name, _type, default_text, *args, **kwargs):

    editor = request.user
    product = Product.objects.get(id=product_id)
    content = ProductContent.objects.filter(
        Q(name=name) &
        Q(product_id=product_id)
    ).first()

    if not content and request.user.is_staff:

        if request.user.is_staff:
            content = ProductContent()
            content.creator = request.user
            content.name = name
            content.desc = default_text
            content.product_id = product.id
            content.save()

    if editor.is_staff:

        if _type == 'desc':
            return get_edit_textarea(name, content, 'update_product_content', _id=product_id)
        if _type in ['image', 'thumb']:
            return get_edit_image(request, name, default_text, content, 'update_product_content', _type, _id=product_id)

    if not content:
        return ''

    if _type == 'url':
        try:
            url = content.image.url
        except:
            url = content.desc
        if 'src' in url:
            return url.split('src="')[1].split('"')[0]
        else:
            return url

    if _type == 'desc':
        return mark_safe(content.desc)

    image = False

    if _type == 'image':
        if content.image:
            image = f'<img src="/media/{content.image}"  />'
    elif _type == 'thumb':
        if content.thumbnail:
            image = f'<img src="/media/{content.thumbnail}"  />'
    if not image:
        image = content.desc
    return mark_safe(image)


@register.simple_tag
def get_category_drop_down_search():
    categories = BlogCategory.objects.filter()

    onchange = f"window.location=this.value"
    html = f'<label for="Categories">Search Categories:</label>' \
           f'<select class="custom-select widget-title" onchange="{onchange}" name="Categories" id="Categories">'
    html += f'<option value="---">Please Select</option>'
    html += f'<option value="/blog/">Reset</option>'
    option = ''
    for cat in categories:

        option += '<option value="{}">{}</option>'.format(
            cat.get_absolute_url(),
            cat.get_title()
        )
    html += option + '</select>'
    return mark_safe(html)


@register.simple_tag
def search_results(request, products, blog_articles,  blog_content):

    results = []

    for product in products:

        if product.thumbnail:
            image_url = product.thumbnail
        else:
            image_url = product.image

        results.append({
            'name': product.name,
            'desc': product.desc,
            'image_url': '/media/' + str(image_url),
            'link': 'http',
        })

    article_list = []
    for article in blog_articles:

        article_list.append(article.id)
        if article.main_image.url:
            image_url = article.main_image.url
        else:
            image_url = article.main_image

        results.append({
            'name': article.__str__(),
            'desc': article.abstract,
            'image_url': image_url,
            'link': 'http',
        })

    for content in blog_content:

        if content.blog.id not in article_list:

            if content.blog.main_image.url:
                image_url = content.blog.main_image.url
            else:
                image_url = content.blog.main_image

            results.append({
                'name': content.blog.__str__(),
                'desc': content.blog.abstract,
                'image_url': image_url,
                'link': 'http',
            })
    search_paginator = Paginator(results, 10)  # Show 25 contacts per page.
    search_page_number = request.GET.get("page")
    search_obj = search_paginator.get_page(search_page_number)

    return search_obj


@register.simple_tag
def get_cart_menu(request):
    placed_order = Order.objects.filter(Q(buyer=request.user) & Q(status='C')).first()
    if placed_order:
        return mark_safe('<a href="/cart/">'
                         '<i class="fa fa-shopping-cart" aria-hidden="true"></i> '
                         '<span>Order '
                         f'<span class="cart-quantity">{placed_order.total_items}'
                         '</span></span>'
                         '</a>')
    else:
        cart = Order.objects.filter(Q(buyer=request.user) & Q(status='P')).first()
        if cart:
            total_items = cart.total_items
        else:
            total_items = 0
        return mark_safe('<a href="/cart/">'
                         '<i class="fa fa-shopping-cart" aria-hidden="true"></i> '
                         '<span>Cart '
                         f'<span class="cart-quantity">{total_items}'
                         '</span></span>'
                         '</a>')
