from django import template
from django.contrib.auth import get_user_model
from django.middleware.csrf import get_token
from django.utils.safestring import mark_safe

from api.models import Content

register = template.Library()
User = get_user_model()


@register.simple_tag
def get_content(request, name, _type, default_text, *args, **kwargs):

    editor = request.user
    content = Content.objects.filter(name=name).first()

    if not content:
        content = Content()
        content.creator = request.user
        content.name = name
        content.desc = default_text
        content.save()

    if _type == 'desc':
        return content.desc
    if _type == 'image':
        image_class = ''
        if 'class' in default_text:
            image_class = default_text.split('class=')[1].split('"')[1]
        return f'<src class="{image_class}" '+content.image.split('<src')[1]


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
        editor_width = len(content.desc)

        if _type == 'desc':

            textarea = f'<textarea ' \
                       f'style="min-width: 100%;" class="" ' \
                       f'rows="6" cols="20" size="{editor_width}" type="text" ' \
                       f'name="editor_{name}" id="editor_{name}">{content.desc}' \
                       f'</textarea>' \
                       f''
            edit_image = '<img src="/media/img/edit.png" style="width:10px;height:10px;background-color:white;" />'
            edit_html = f"""{content.desc}<div style="" onclick='edit_data_{name}();' class='content_text_{name}'>
            {edit_image}</div>
            <script>
                function edit_data_{name}(){{  
                    $("#myModal").modal("show");
                    $(".modal-body").html($('.content_editor_{name}_div').html());
                }}
            </script>
            <div class="content_editor_{name}_div" style="display:none;">
            <form action="/api/update" method="get">
                {textarea}
                <button class="btn alazea-btn" type="submit">Save</button>
            </form>
            </div>"""
            return mark_safe(edit_html.replace("{{", "{").replace("}}", "}"))

        if _type == 'image':
            token = get_token(request)

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
            <form class="content_editor_{name}" action="/api/update" method="post" enctype="multipart/form-data">
              <input type="file" id="image_content_editor_{name}" name="image_content_editor_{name}" accept="image/*">
              <input type="hidden" name="csrfmiddlewaretoken" value="{token}">
              <input type="submit" class="btn alazea-btn">
            </form>
            </div>"""
            return mark_safe(edit_html.replace("{{", "{").replace("}}", "}"))

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
            <form action="/api/update" method="get">
                {input}
            </form>
            </div>"""
            return mark_safe(edit_html.replace("{{", "{").replace("}}", "}"))

    if not content:
        return ''

    if _type == 'desc':
        return mark_safe(content.desc)
