# Generated by Django 2.2.6 on 2023-01-20 10:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0032_auto_20230120_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_pass',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 1, 20, 13, 32, 4, 722273), null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 20, 13, 32, 4, 721273), verbose_name='Дата'),
        ),
    ]
