# Generated by Django 2.2.6 on 2023-10-06 09:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0084_auto_20231004_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_pass',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 10, 6, 12, 0, 39, 530687), null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 6, 12, 0, 39, 529687), verbose_name='Дата'),
        ),
    ]