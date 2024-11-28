# Generated by Django 2.2.6 on 2022-12-16 06:27

import datetime
from django.db import migrations, models
import storage.models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0048_auto_20221205_1543'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='th',
            name='cz',
        ),
        migrations.RemoveField(
            model_name='th',
            name='money',
        ),
        migrations.RemoveField(
            model_name='th',
            name='num',
        ),
        migrations.AlterField(
            model_name='event',
            name='pub_day',
            field=models.TextField(default=datetime.date(2022, 12, 16), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='th',
            name='pub_day',
            field=models.TextField(default=datetime.date(2022, 12, 16), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='th',
            name='th',
            field=models.FileField(blank=True, null=True, upload_to=storage.models.get_path, verbose_name='Накладная'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='pub_day',
            field=models.TextField(default=datetime.date(2022, 12, 16), verbose_name='Дата'),
        ),
    ]