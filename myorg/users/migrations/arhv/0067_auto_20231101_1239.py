# Generated by Django 2.2.6 on 2023-11-01 09:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0066_auto_20231101_1234'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_widgets',
            old_name='cors',
            new_name='corr',
        ),
        migrations.AddField(
            model_name='user_info',
            name='test_access',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Доступ ктестам'),
        ),
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 11, 1, 12, 39, 28, 993865), null=True, verbose_name='Дата'),
        ),
    ]
