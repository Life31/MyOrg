# Generated by Django 2.2.6 on 2022-07-29 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configs', '0003_auto_20220729_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config',
            name='other_info',
            field=models.TextField(blank=True, null=True, verbose_name='Проч. идент. конф.'),
        ),
    ]
