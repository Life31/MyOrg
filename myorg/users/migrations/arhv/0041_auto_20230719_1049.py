# Generated by Django 2.2.6 on 2023-07-19 07:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0040_auto_20230530_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 7, 19, 10, 48, 57, 344011), null=True, verbose_name='Дата'),
        ),
    ]
