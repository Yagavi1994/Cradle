# Generated by Django 4.2.15 on 2024-08-28 16:30

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='featured_image',
            field=cloudinary.models.CloudinaryField(default='default_jubihg', max_length=255, verbose_name='image'),
        ),
    ]
