# Generated by Django 2.2.6 on 2023-04-24 11:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_auto_20230227_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 4, 24, 14, 26, 31, 703961), null=True, verbose_name='Дата'),
        ),
    ]