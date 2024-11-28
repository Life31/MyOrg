# Generated by Django 2.2.6 on 2022-12-02 09:56

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0046_auto_20221130_1509'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=200, verbose_name='Тег')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ('pk',),
            },
        ),
        migrations.AlterField(
            model_name='event',
            name='pub_day',
            field=models.TextField(default=datetime.date(2022, 12, 2), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='th',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='th',
            name='day',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='th',
            name='pub_day',
            field=models.TextField(default=datetime.date(2022, 12, 2), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='th',
            name='type_th',
            field=models.TextField(blank=True, choices=[('Входящие', 'Входящие'), ('Исходящие', 'Исходящие')], null=True, verbose_name='Вх. / Исх.'),
        ),
        migrations.AlterField(
            model_name='th',
            name='year',
            field=models.TextField(blank=True, choices=[('2021', '2021'), ('2022', '2022'), ('2023', '2023')], null=True, verbose_name='Год'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='pub_day',
            field=models.TextField(default=datetime.date(2022, 12, 2), verbose_name='Дата'),
        ),
        migrations.CreateModel(
            name='Th_tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='th_tags', to='storage.Tag', verbose_name='Таг')),
                ('th', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ths_tag', to='storage.Th', verbose_name='Накладная')),
            ],
            options={
                'verbose_name': 'Запись типа:Тег - накладная',
                'verbose_name_plural': 'Записи типа:Тег - накладная',
                'ordering': ('tag',),
            },
        ),
    ]