# Generated by Django 2.2.6 on 2023-02-01 10:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0052_auto_20230120_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='pub_day',
            field=models.TextField(default=datetime.date(2023, 2, 1), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='th',
            name='pub_day',
            field=models.TextField(default=datetime.date(2023, 2, 1), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='pub_day',
            field=models.TextField(default=datetime.date(2023, 2, 1), verbose_name='Дата'),
        ),
    ]