# Generated by Django 2.2.6 on 2023-05-17 13:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0029_auto_20230517_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 17, 16, 57, 31, 931942), null=True, verbose_name='Дата'),
        ),
    ]