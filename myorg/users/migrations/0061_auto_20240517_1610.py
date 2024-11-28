# Generated by Django 2.2.6 on 2024-05-17 13:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0060_auto_20240517_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_widgets',
            name='calc_open',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Калькулятор открыт'),
        ),
        migrations.AddField(
            model_name='user_widgets',
            name='corr_open',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Корреспонденция открыт'),
        ),
        migrations.AddField(
            model_name='user_widgets',
            name='mess_open',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Мессенджер открыт'),
        ),
        migrations.AddField(
            model_name='user_widgets',
            name='news_open',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Новости открыт'),
        ),
        migrations.AddField(
            model_name='user_widgets',
            name='notes_open',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Заметки открыт'),
        ),
        migrations.AddField(
            model_name='user_widgets',
            name='reqs_open',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Заявки на испытания открыт'),
        ),
        migrations.AddField(
            model_name='user_widgets',
            name='stor_open',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Склад открыт'),
        ),
        migrations.AddField(
            model_name='user_widgets',
            name='task_open',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Задачи открыт'),
        ),
        migrations.AddField(
            model_name='user_widgets',
            name='test_open',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Тесты открыт'),
        ),
        migrations.AddField(
            model_name='user_widgets',
            name='users_open',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Сотрудники открыт'),
        ),
        migrations.AddField(
            model_name='user_widgets',
            name='vacs_open',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Отпуска открыт'),
        ),
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 5, 17, 16, 10, 43, 218314), null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='user_widgets',
            name='bibl_open',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Библиотека открыта'),
        ),
        migrations.AlterField(
            model_name='user_widgets',
            name='users',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Сотрудники'),
        ),
    ]