# Generated by Django 2.2.6 on 2023-08-30 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configs', '0017_unit_pos_on_storage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='part_n',
            field=models.TextField(blank=True, null=True, verbose_name='P/N'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='serial_n',
            field=models.TextField(blank=True, null=True, verbose_name='S/N'),
        ),
    ]