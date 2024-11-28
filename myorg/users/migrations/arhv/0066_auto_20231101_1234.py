# Generated by Django 2.2.6 on 2023-11-01 09:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0065_auto_20231101_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_widgets',
            name='bibl',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Библиотека'),
        ),
        migrations.AddField(
            model_name='user_widgets',
            name='cors',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Корреспонденция'),
        ),
        migrations.AddField(
            model_name='user_widgets',
            name='stor',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Склад'),
        ),
        migrations.AddField(
            model_name='user_widgets',
            name='task',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Задачи'),
        ),
        migrations.AddField(
            model_name='user_widgets',
            name='test',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Тесты'),
        ),
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 11, 1, 12, 34, 12, 734011), null=True, verbose_name='Дата'),
        ),
    ]