# Generated by Django 2.2.6 on 2023-11-01 08:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0064_auto_20231101_1145'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_info',
            old_name='vaqs_access',
            new_name='vacs_access',
        ),
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 11, 1, 11, 47, 18, 474832), null=True, verbose_name='Дата'),
        ),
    ]