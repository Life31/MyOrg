# Generated by Django 2.2.6 on 2024-01-15 06:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0084_auto_20231205_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='pub_day',
            field=models.TextField(default=datetime.date(2024, 1, 15), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='th',
            name='pub_day',
            field=models.TextField(default=datetime.date(2024, 1, 15), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='th',
            name='year',
            field=models.TextField(blank=True, choices=[('2023', '2023'), ('2024', '2024'), ('2025', '2025')], null=True, verbose_name='Год'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='pub_day',
            field=models.TextField(default=datetime.date(2024, 1, 15), verbose_name='Дата'),
        ),
    ]
