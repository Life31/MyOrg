# Generated by Django 2.2.6 on 2024-05-14 13:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0117_auto_20240513_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_pass',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 5, 14, 16, 36, 55, 709229), null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 14, 16, 36, 55, 708229), verbose_name='Дата'),
        ),
    ]