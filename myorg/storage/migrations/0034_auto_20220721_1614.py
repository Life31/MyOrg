# Generated by Django 2.2.6 on 2022-07-21 13:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0033_auto_20220720_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='th',
            name='pub_day',
            field=models.TextField(default=datetime.date(2022, 7, 21), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='pub_day',
            field=models.TextField(default=datetime.date(2022, 7, 21), verbose_name='Дата'),
        ),
    ]
