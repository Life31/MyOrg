# Generated by Django 2.2.6 on 2024-05-31 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_auto_20240531_1020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='include_in',
        ),
    ]
