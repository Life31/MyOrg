# Generated by Django 2.2.6 on 2021-08-19 14:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0031_auto_20210819_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.date(2021, 8, 19), help_text='формат ввода: YYYY-mm-dd', null=True, verbose_name='Дата испытаний'),
        ),
    ]
