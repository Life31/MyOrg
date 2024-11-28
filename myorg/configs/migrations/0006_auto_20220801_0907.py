# Generated by Django 2.2.6 on 2022-08-01 06:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('configs', '0005_auto_20220729_1112'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='number',
            options={'ordering': ('number',), 'verbose_name': 'Номер конфигурации', 'verbose_name_plural': 'Номера конфигурации'},
        ),
        migrations.AlterField(
            model_name='number',
            name='number',
            field=models.TextField(verbose_name='номер конфигурации'),
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.TextField(verbose_name='Статус')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='q_numbers', to='configs.Number', verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Запрос на изменение конфигурации',
                'verbose_name_plural': 'Запросы на изменение конфигурации',
                'ordering': ('number',),
            },
        ),
    ]