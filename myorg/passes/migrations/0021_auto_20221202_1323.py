# Generated by Django 2.2.6 on 2022-12-02 10:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0020_auto_20221202_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_pass',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 12, 2, 10, 23, 54, 753828, tzinfo=utc), null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 2, 13, 23, 54, 753828), verbose_name='Дата'),
        ),
    ]
