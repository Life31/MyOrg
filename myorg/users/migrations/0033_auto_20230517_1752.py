# Generated by Django 2.2.6 on 2023-05-17 14:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0032_auto_20230517_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 17, 17, 52, 18, 747591), null=True, verbose_name='Дата'),
        ),
    ]
