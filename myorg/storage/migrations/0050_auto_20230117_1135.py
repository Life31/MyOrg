# Generated by Django 2.2.6 on 2023-01-17 08:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0049_auto_20221216_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='pub_day',
            field=models.TextField(default=datetime.date(2023, 1, 17), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='th',
            name='pub_day',
            field=models.TextField(default=datetime.date(2023, 1, 17), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='th',
            name='year',
            field=models.TextField(blank=True, choices=[('2022', '2022'), ('2023', '2023'), ('2024', '2024')], null=True, verbose_name='Год'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='pub_day',
            field=models.TextField(default=datetime.date(2023, 1, 17), verbose_name='Дата'),
        ),
    ]