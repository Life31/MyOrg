# Generated by Django 2.2.6 on 2022-10-19 09:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0011_auto_20221019_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pass',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 19, 12, 38, 36, 205918), help_text='формат ввода: YYYY-mm-dd', null=True, verbose_name='Дата'),
        ),
    ]