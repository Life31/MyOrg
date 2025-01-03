# Generated by Django 2.2.6 on 2024-05-17 10:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0059_auto_20240517_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_widgets',
            name='bibl_open',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Библиотека_открыта'),
        ),
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 5, 17, 13, 50, 44, 374234), null=True, verbose_name='Дата'),
        ),
    ]
