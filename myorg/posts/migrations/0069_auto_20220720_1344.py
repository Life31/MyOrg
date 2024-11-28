# Generated by Django 2.2.6 on 2022-07-20 10:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0068_post_all_in'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('likes', models.IntegerField(blank=True, default=0, null=True, verbose_name='лайки')),
                ('dislikes', models.IntegerField(blank=True, default=0, null=True, verbose_name='дизлайки')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('state', models.ForeignKey(blank=True, default=5, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fb_states', to='posts.Task_state', verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Обращение',
                'verbose_name_plural': 'Обращения',
                'ordering': ['-created'],
            },
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-day', '-text', '-t_start'), 'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='f_likes', to='posts.Feedback', verbose_name='Отзыв')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='u_likes', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
        ),
        migrations.CreateModel(
            name='Dislike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='f_dislikes', to='posts.Feedback', verbose_name='Отзыв')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='u_dislikes', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
        ),
    ]