# Generated by Django 2.2.6 on 2022-04-04 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0062_auto_20220404_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='t_start_html',
            field=models.IntegerField(blank=True, null=True, verbose_name='время начала_html'),
        ),
        migrations.AlterField(
            model_name='post',
            name='t_stop_html',
            field=models.IntegerField(blank=True, null=True, verbose_name='время завершения_html'),
        ),
    ]