# Generated by Django 3.0.5 on 2021-01-13 10:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0011_auto_20210112_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='read_by',
            field=models.ManyToManyField(related_name='read_message', to=settings.AUTH_USER_MODEL),
        ),
    ]
