# Generated by Django 2.2.6 on 2023-05-19 14:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0066_auto_20230519_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_pass',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 19, 17, 3, 6, 193602), null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 19, 17, 3, 6, 192602), verbose_name='Дата'),
        ),
    ]