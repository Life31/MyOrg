# Generated by Django 2.2.6 on 2023-10-09 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_bord_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='bord',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bord_cards', to='tasks.Bord', verbose_name='Доска'),
        ),
    ]
