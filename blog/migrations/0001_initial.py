# Generated by Django 4.2.15 on 2024-08-14 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('source', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('category', models.IntegerField(choices=[(0, 'Newborn'), (1, 'Breastfeeding'), (2, 'Formula Feeding'), (3, 'Sleep'), (4, 'Baby Led Weaning'), (5, 'Eating Habits'), (6, 'Potty Training'), (7, 'Toddlers'), (8, 'Parenting'), (9, 'Personal Stories'), (10, 'Teens')], default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(0, 'Draft'), (1, 'Published')], default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
    ]
