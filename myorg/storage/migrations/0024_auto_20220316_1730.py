# Generated by Django 2.2.6 on 2022-03-16 14:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0023_auto_20220315_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='th',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.date(2022, 3, 16), help_text='формат ввода: YYYY-mm-dd', null=True, verbose_name='Дата испытаний'),
        ),
        migrations.AlterField(
            model_name='th',
            name='pub_day',
            field=models.TextField(default=datetime.date(2022, 3, 16), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='pub_day',
            field=models.TextField(default=datetime.date(2022, 3, 16), verbose_name='Дата'),
        ),
    ]
