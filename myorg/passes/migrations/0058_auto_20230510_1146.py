# Generated by Django 2.2.6 on 2023-05-10 08:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0057_auto_20230510_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_pass',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 10, 11, 46, 13, 401507), null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 10, 11, 46, 13, 401507), verbose_name='Дата'),
        ),
    ]
