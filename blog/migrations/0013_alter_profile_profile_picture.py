# Generated by Django 4.2.15 on 2024-08-27 15:36

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=cloudinary.models.CloudinaryField(default='nnn7jme2crgxnlba6ygb', max_length=255, verbose_name='image'),
        ),
    ]
