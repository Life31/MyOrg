# Generated by Django 2.2.6 on 2023-02-20 12:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0042_auto_20230213_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_pass',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 2, 20, 15, 2, 14, 351383), null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 20, 15, 2, 14, 350383), verbose_name='Дата'),
        ),
    ]
