# Generated by Django 2.2.6 on 2023-01-17 08:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0024_auto_20221216_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_pass',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 1, 17, 11, 35, 42, 382048), null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 17, 11, 35, 42, 380047), verbose_name='Дата'),
        ),
    ]