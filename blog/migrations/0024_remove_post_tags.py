# Generated by Django 4.2.15 on 2024-09-03 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_alter_profile_selected_avatar_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='tags',
        ),
    ]