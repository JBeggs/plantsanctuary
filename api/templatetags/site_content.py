from django import template
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.middleware.csrf import get_token
from django.utils.safestring import mark_safe
from djangocms_blog.models import Post, BlogCategory
from django.utils.text import slugify
from api.models import Content, BlogContent

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


def get_edit_textarea(name, content, form_action, blog_id):

    blog_input = f'<input type="hidden" name="blog_id" value="{blog_id}">'
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


def get_edit_image(request, name, default_text, content, form_action, blog_id):
    token = get_token(request)
    blog_input = f'<input type="hidden" name="blog_id" value="{blog_id}">'
    image_class = ''
    if 'class' in default_text:
        image_class = default_text.split('class=')[1].split('"')[1]

    if content.image:
        image = f'<img class="{image_class}" src="/media/{content.image}" />'
    else:
        image = content.desc
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
      <input onclick="window.location='/api/delete/{content.id}/'" type="button" class="btn alazea-btn" value="Delete"></p>
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
            return get_edit_textarea(name, content, 'update_content', blog_id=None)
        if _type == 'image':
            return get_edit_image(request, name, default_text, content, 'update_content', blog_id=None)

    if not content:
        return ''

    if _type == 'desc':
        return mark_safe(content.desc)

    if _type == 'image':
        if content.image:
            image_class = ''
            if 'class' in default_text:
                image_class = default_text.split('class=')[1].split('"')[1]
            image = f'<img class="{image_class}" src="/media/{content.image}" />'
        else:
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

    if not content and request.user.is_staff:
        if request.user == content.author:
            content = BlogContent()
            content.author = request.user
            content.blog = Post.objects.get(id=blog_id)
            content.name = name
            content.desc = default_text
            content.save()

    if editor.is_staff and request.user == content.author:

        if _type == 'desc':
            return get_edit_textarea(name, content, 'update_blog_content', blog_id=blog_id)
        if _type == 'image':
            return get_edit_image(request, name, default_text, content, 'update_blog_content', blog_id=blog_id)

    if not content:
        return ''

    if _type == 'desc':
        return mark_safe(content.desc)

    if _type == 'image':
        if content.image:
            image_class = ''
            if 'class' in default_text:
                image_class = default_text.split('class=')[1].split('"')[1]
            image = f'<img class="{image_class}" src="/media/{content.image}" />'
        else:
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


