# Generated by Django 2.2.6 on 2023-11-02 12:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0069_auto_20231101_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='readed',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Прочитанно'),
        ),
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 11, 2, 15, 5, 38, 166734), null=True, verbose_name='Дата'),
        ),
    ]
