# Generated by Django 2.2.6 on 2024-05-31 07:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0065_auto_20240530_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 5, 31, 10, 20, 13, 75917), null=True, verbose_name='Дата'),
        ),
    ]
