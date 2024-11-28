# Generated by Django 2.2.6 on 2024-04-23 11:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, default='Новая заметка', null=True, verbose_name='Заметка')),
                ('day_start', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Дата создания')),
                ('day_update', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Дата последнего изменения')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_notes', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Заметка',
                'verbose_name_plural': 'Заметки',
                'ordering': ('day_update',),
            },
        ),
    ]