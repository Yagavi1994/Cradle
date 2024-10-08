# Generated by Django 4.2.15 on 2024-08-29 19:36

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_profile_selected_avatar1_profile_selected_avatar2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='selected_avatar',
            field=cloudinary.models.CloudinaryField(default='profile_pictures/mlu4iynnxdgpam21jrli', max_length=255, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='selected_avatar1',
            field=cloudinary.models.CloudinaryField(default='profile_pictures/cd4uhjgqvhj0kbwcmtqk', max_length=255, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='selected_avatar2',
            field=cloudinary.models.CloudinaryField(default='profile_pictures/y7wgg6bw81hry1cs5bap', max_length=255, verbose_name='image'),
        ),
    ]
