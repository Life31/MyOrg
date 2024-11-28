# Generated by Django 2.2.6 on 2022-12-02 09:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0019_auto_20221130_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_pass',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 12, 2, 9, 56, 7, 722628, tzinfo=utc), null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 2, 12, 56, 7, 707028), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='doc_type',
            field=models.TextField(blank=True, default='Паспорт', null=True, verbose_name='Документ'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='spec',
            field=models.TextField(blank=True, choices=[('Д.А. Мыльников', 'Д.А. Мыльников'), ('Л.А. Елагин', 'Л.А. Елагин')], default='Д.А. Мыльников', null=True, verbose_name='Подписант'),
        ),
    ]