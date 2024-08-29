# Generated by Django 4.2.15 on 2024-08-29 22:24

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_alter_profile_selected_avatar2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='selected_avatar',
            field=cloudinary.models.CloudinaryField(default='avatar1_dw6wb7', max_length=255, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='selected_avatar1',
            field=cloudinary.models.CloudinaryField(default='kjxyk9iaiqwwximms8cc', max_length=255, verbose_name='image'),
        ),
    ]
