# Generated by Django 2.2.6 on 2023-10-04 12:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unswers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unswer_1', models.TextField(blank=True, null=True, verbose_name='ответ 1')),
                ('unswer_2', models.TextField(blank=True, null=True, verbose_name='ответ 2')),
                ('unswer_3', models.TextField(blank=True, null=True, verbose_name='ответ 3')),
                ('unswer_4', models.TextField(blank=True, null=True, verbose_name='ответ 4')),
                ('unswer_5', models.TextField(blank=True, null=True, verbose_name='ответ 5')),
                ('unswer_6', models.TextField(blank=True, null=True, verbose_name='ответ 6')),
                ('unswer_7', models.TextField(blank=True, null=True, verbose_name='ответ 7')),
                ('unswer_8', models.TextField(blank=True, null=True, verbose_name='ответ 8')),
                ('unswer_9', models.TextField(blank=True, null=True, verbose_name='ответ 9')),
                ('unswer_10', models.TextField(blank=True, null=True, verbose_name='ответ 10')),
                ('unswer_11', models.TextField(blank=True, null=True, verbose_name='ответ 11')),
                ('unswer_12', models.TextField(blank=True, null=True, verbose_name='ответ 12')),
                ('unswer_13', models.TextField(blank=True, null=True, verbose_name='ответ 13')),
                ('unswer_14', models.TextField(blank=True, null=True, verbose_name='ответ 14')),
                ('unswer_15', models.TextField(blank=True, null=True, verbose_name='ответ 15')),
                ('unswer_16', models.TextField(blank=True, null=True, verbose_name='ответ 16')),
                ('unswer_17', models.TextField(blank=True, null=True, verbose_name='ответ 17')),
                ('unswer_18', models.TextField(blank=True, null=True, verbose_name='ответ 18')),
                ('unswer_19', models.TextField(blank=True, null=True, verbose_name='ответ 19')),
                ('unswer_20', models.TextField(blank=True, null=True, verbose_name='ответ 20')),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='unswers', to='tests.Test', verbose_name='Тест')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_unswers', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Ответы',
                'verbose_name_plural': 'Ответы',
            },
        ),
    ]
