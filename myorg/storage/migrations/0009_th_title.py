# Generated by Django 2.2.6 on 2021-09-06 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0008_auto_20210906_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='th',
            name='title',
            field=models.TextField(default=1, verbose_name='Наименование'),
            preserve_default=False,
        ),
    ]
