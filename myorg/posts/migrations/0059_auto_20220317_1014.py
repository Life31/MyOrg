# Generated by Django 2.2.6 on 2022-03-17 07:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0058_auto_20220316_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='day',
            field=models.DateTimeField(default=datetime.date(2022, 3, 17), verbose_name='Дата испытаний'),
        ),
    ]
