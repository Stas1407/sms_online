# Generated by Django 3.1.7 on 2021-03-31 18:22

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20210331_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='image',
            field=models.ImageField(default='default_group.svg', upload_to=main.models.check_path),
        ),
    ]
