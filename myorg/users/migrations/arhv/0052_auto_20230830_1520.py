# Generated by Django 2.2.6 on 2023-08-30 12:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0051_auto_20230830_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 30, 15, 19, 59, 389953), null=True, verbose_name='Дата'),
        ),
    ]