# Generated by Django 2.2.6 on 2023-01-17 08:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='slave',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_tasks', to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель'),
        ),
    ]