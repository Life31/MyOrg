# Generated by Django 2.2.6 on 2022-10-20 07:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0012_auto_20221019_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pass',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 20, 10, 18, 42, 991451), help_text='формат ввода: YYYY-mm-dd', null=True, verbose_name='Дата'),
        ),
    ]