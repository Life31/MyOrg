# Generated by Django 2.2.6 on 2022-04-04 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0061_auto_20220404_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='t_start_html',
            field=models.FloatField(blank=True, null=True, verbose_name='время начала_html'),
        ),
        migrations.AlterField(
            model_name='post',
            name='t_stop_html',
            field=models.FloatField(blank=True, null=True, verbose_name='время завершения_html'),
        ),
    ]