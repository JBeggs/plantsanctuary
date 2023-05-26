# Generated by Django 3.2.19 on 2023-05-25 21:17

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_blogcontent'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to=api.models.content_image_thumbnail_path),
        ),
    ]
