# Generated by Django 2.2.6 on 2021-10-05 13:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0049_auto_20211005_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.date(2021, 10, 5), null=True, verbose_name='Дата испытаний'),
        ),
    ]