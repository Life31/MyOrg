# Generated by Django 2.2.6 on 2023-12-05 18:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0076_auto_20231204_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 12, 5, 21, 3, 7, 956367), null=True, verbose_name='Дата'),
        ),
    ]