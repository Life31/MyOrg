# Generated by Django 2.2.6 on 2023-02-20 12:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20230213_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 2, 20, 15, 2, 14, 334381), null=True, verbose_name='Дата'),
        ),
    ]
