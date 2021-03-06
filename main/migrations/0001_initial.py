# Generated by Django 3.0.5 on 2021-01-08 19:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Unread_messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('date_sent', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('image', models.ImageField(default='default.jpg', upload_to=main.models.check_path)),
                ('last_message', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Message')),
                ('unread_messages', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Unread_messages')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to=main.models.check_path)),
                ('last_message', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Message')),
                ('unread_messages', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Unread_messages')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
