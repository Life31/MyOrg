# Generated by Django 2.2.6 on 2023-07-19 12:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0042_auto_20230719_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 7, 19, 15, 25, 15, 175131), null=True, verbose_name='Дата'),
        ),
    ]
