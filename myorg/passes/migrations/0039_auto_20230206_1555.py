# Generated by Django 2.2.6 on 2023-02-06 12:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0038_auto_20230206_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_pass',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 2, 6, 15, 55, 18, 67875), null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 6, 15, 55, 18, 66874), verbose_name='Дата'),
        ),
    ]