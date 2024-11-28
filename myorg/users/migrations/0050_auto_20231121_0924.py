# Generated by Django 2.2.6 on 2023-11-21 06:24

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0049_auto_20231108_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_info',
            name='bibl_access',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Доступ к библиотеке'),
        ),
        migrations.AddField(
            model_name='user_info',
            name='test_access',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Доступ к тестам'),
        ),
        migrations.AddField(
            model_name='user_info',
            name='vacs_access',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Доступ к отпускам'),
        ),
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 11, 21, 9, 24, 26, 688410), null=True, verbose_name='Дата'),
        ),
        migrations.CreateModel(
            name='User_widgets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reqs', models.BooleanField(blank=True, default=False, null=True, verbose_name='Заявки на испытания')),
                ('vacs', models.BooleanField(blank=True, default=False, null=True, verbose_name='Отпуска')),
                ('test', models.BooleanField(blank=True, default=False, null=True, verbose_name='Тесты')),
                ('corr', models.BooleanField(blank=True, default=False, null=True, verbose_name='Корреспонденция')),
                ('task', models.BooleanField(blank=True, default=False, null=True, verbose_name='Задачи')),
                ('bibl', models.BooleanField(blank=True, default=False, null=True, verbose_name='Библиотека')),
                ('stor', models.BooleanField(blank=True, default=False, null=True, verbose_name='Склад')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_widgets', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Доступ к виджетам',
                'ordering': ('user',),
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Номер заявки')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('readed', models.BooleanField(blank=True, default=False, null=True, verbose_name='Прочитанно')),
                ('user_one', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_one_mess', to=settings.AUTH_USER_MODEL, verbose_name='Первый пользователь')),
                ('user_two', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_two_mess', to=settings.AUTH_USER_MODEL, verbose_name='Второй пользователь')),
                ('witch_write', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_witch_write', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь который написал')),
            ],
            options={
                'verbose_name': 'Переписка',
                'ordering': ('pub_date',),
            },
        ),
    ]