# Generated by Django 2.2.6 on 2024-05-31 11:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0127_auto_20240531_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_pass',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 5, 31, 14, 41, 33, 462122), null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 31, 14, 41, 33, 461123), verbose_name='Дата'),
        ),
    ]
