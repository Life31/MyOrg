# Generated by Django 2.2.6 on 2023-12-04 06:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0103_auto_20231204_0903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_pass',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 12, 4, 9, 6, 19, 264746), null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 4, 9, 6, 19, 264746), verbose_name='Дата'),
        ),
    ]
