# Generated by Django 2.2.6 on 2022-08-01 09:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('configs', '0006_auto_20220801_0907'),
    ]

    operations = [
        migrations.CreateModel(
            name='Change',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_n', models.TextField(verbose_name='P/N')),
                ('other_info', models.TextField(blank=True, null=True, verbose_name='Проч. идент. конф.')),
                ('descr', models.TextField(verbose_name='Примечание')),
                ('doc', models.FileField(blank=True, null=True, upload_to='config/доводочные работы/', verbose_name='Документ')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('state', models.TextField(verbose_name='Статус')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ch_configs', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('include_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ch_includes', to='configs.Include', verbose_name='Влож. эл. конф.')),
                ('number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='changes', to='configs.Query', verbose_name='Номер запроса')),
                ('unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ch_units', to='configs.Unit', verbose_name='Блок')),
            ],
            options={
                'verbose_name': 'изменение конфигурации',
                'verbose_name_plural': 'изменения конфигурации',
                'ordering': ('number',),
            },
        ),
    ]
