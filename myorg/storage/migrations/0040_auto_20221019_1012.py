# Generated by Django 2.2.6 on 2022-10-19 07:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0039_auto_20221018_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='pub_day',
            field=models.TextField(default=datetime.date(2022, 10, 19), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='th',
            name='pub_day',
            field=models.TextField(default=datetime.date(2022, 10, 19), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='pub_day',
            field=models.TextField(default=datetime.date(2022, 10, 19), verbose_name='Дата'),
        ),
    ]