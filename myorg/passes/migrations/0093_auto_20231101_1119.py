# Generated by Django 2.2.6 on 2023-11-01 08:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0092_auto_20231023_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_pass',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 11, 1, 11, 19, 29, 986527), null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 1, 11, 19, 29, 985528), verbose_name='Дата'),
        ),
    ]
