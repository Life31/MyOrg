# Generated by Django 2.2.6 on 2024-05-13 11:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0055_auto_20240423_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 5, 13, 14, 53, 52, 243965), null=True, verbose_name='Дата'),
        ),
    ]
