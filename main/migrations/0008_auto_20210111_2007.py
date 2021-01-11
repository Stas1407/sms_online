# Generated by Django 3.0.5 on 2021-01-11 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20210111_1134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversation',
            name='last_message',
        ),
        migrations.RemoveField(
            model_name='conversation',
            name='last_message_date',
        ),
        migrations.RemoveField(
            model_name='group',
            name='last_message',
        ),
        migrations.RemoveField(
            model_name='group',
            name='last_message_date',
        ),
        migrations.AddField(
            model_name='conversation',
            name='messages',
            field=models.ManyToManyField(default=None, null=True, to='main.Message'),
        ),
        migrations.AddField(
            model_name='group',
            name='messages',
            field=models.ManyToManyField(default=None, null=True, to='main.Message'),
        ),
    ]
