# Generated by Django 2.2.6 on 2021-08-30 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Th',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Наименование')),
                ('num', models.TextField(verbose_name='Количество')),
                ('money', models.TextField(verbose_name='Стоимость')),
                ('cz', models.TextField(verbose_name='Служебная записка')),
                ('th', models.TextField(verbose_name='Накладная')),
                ('day', models.TextField(verbose_name='Дата')),
                ('comment', models.TextField(verbose_name='Комментарий')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Наименование')),
                ('creator', models.TextField(verbose_name='Производитель')),
                ('code', models.TextField(verbose_name='Обозначение')),
                ('ctgry', models.TextField(verbose_name='Категория')),
                ('place', models.TextField(verbose_name='Место хранения')),
                ('si', models.TextField(verbose_name='Еденицы измерения')),
                ('num', models.TextField(verbose_name='Количество')),
                ('comment', models.TextField(verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'Учетная еденица',
                'verbose_name_plural': 'Учетные еденицы',
                'ordering': ('name',),
            },
        ),
    ]