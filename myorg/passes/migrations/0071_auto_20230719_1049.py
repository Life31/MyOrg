# Generated by Django 2.2.6 on 2023-07-19 07:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0070_auto_20230530_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_pass',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 7, 19, 10, 48, 57, 462011), null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 19, 10, 48, 57, 461011), verbose_name='Дата'),
        ),
    ]