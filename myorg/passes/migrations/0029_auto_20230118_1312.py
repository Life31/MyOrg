# Generated by Django 2.2.6 on 2023-01-18 10:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0028_auto_20230118_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_pass',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 1, 18, 13, 12, 11, 514964), null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 18, 13, 12, 11, 513964), verbose_name='Дата'),
        ),
    ]
