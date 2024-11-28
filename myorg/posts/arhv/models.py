from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from calendar import monthrange

from pytils.translit import slugify

import datetime as dt
User = get_user_model()


class Post(models.Model):
    text = models.TextField(verbose_name='Номер заявки', unique=True,
                            help_text="номер заявки присваивается автоматически в порядке возрастания",) # Number unique=True,
    pub_date = models.DateTimeField(auto_now_add=True, # Create_date
                                    verbose_name='Дата начала')
    task_state = models.ForeignKey('Task_state', # Status
                                   blank=True,
                                   null=True,
                                   on_delete=models.SET_NULL,
                                   related_name='states',
                                   verbose_name='Статус',
                                   default=1,)
    author = models.ForeignKey(User, # Creator
                               on_delete=models.CASCADE,
                               related_name='posts',
                               verbose_name='Автор',)
    group = models.ForeignKey('Group', # Stand
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True,
                              related_name='posts',
                              verbose_name='Группа')
    file = models.FileField(verbose_name='Документ', # Documents
                            upload_to='files/',
                            blank=True,
                            null=True,)
    day = models.DateTimeField(verbose_name='Дата испытаний',
                               default=timezone.now, )
                               #default=dt.datetime.now().date(),
                               #help_text="формат ввода: YYYY-mm-dd")
    
    t_start = models.ForeignKey('Time',
                               on_delete=models.SET_NULL,
                               null=True,
                               #blank=True,
                               related_name='time',
                               verbose_name='время начала',
                               help_text="время начала испытаний должно быть строго меньше времени завершения",
                               default=17,)
    t_stop = models.ForeignKey('Time',
                               on_delete=models.SET_NULL,
                               null=True,
                               #blank=True,
                               related_name='times',
                               verbose_name='время окончания',
                               help_text="время завершения испытаний должно быть строго больше времени начала",
                               default=27,)
    t_start_html = models.IntegerField(
                               null=True,
                               blank=True,
                               verbose_name='время начала_html',)
    t_stop_html = models.IntegerField(
                               null=True,
                               blank=True,
                               verbose_name='время завершения_html',)
    testers = models.TextField(verbose_name='Состав бригады испытателей', )
    test_object = models.TextField(verbose_name='Объект испытаний', )
    unit = models.ForeignKey('Unit', on_delete=models.SET_NULL, null=True,
                             related_name='units', verbose_name='Подразделение - инициатор')
    purpose = models.TextField(verbose_name='Цель проведения испытаний', )
    reason = models.TextField(verbose_name='Основания для проведения испытаний', )
    configuration = models.TextField(verbose_name='Минимальная конфигурация стенда', )
    instruments = models.TextField(verbose_name='Необходимый инструмент', blank=True, null=True)
    add_requirements = models.TextField(verbose_name='Дополнительные требования', blank=True, null=True)
    doc = models.TextField(verbose_name='Документ', blank=True, null=True)
    all_in = models.TextField(verbose_name='Стенды в заявке', blank=True, null=True, )
    
    class Meta:
        ordering = ('-day', '-text', '-t_start' )
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self) -> str:
        return self.text[:30]

    def save(self, *args, **kwargs):
        if not self.all_in:
            self.all_in = self.text
        super().save(*args, **kwargs)

class Unit(models.Model):
    title = models.CharField(max_length=200, verbose_name='Номер отдела')
    description = models.CharField(blank=True,
                                   null=True,
                                   max_length=200,
                                   verbose_name='Название отдела')
    class Meta:
        ordering = ('title',)
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

    def __str__(self) -> str:
        return self.title


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название стенда')    
    slug = models.SlugField(unique=True, verbose_name='Путь')
    description = models.CharField(blank=True,
                                   null=True,
                                   max_length=200,
                                   verbose_name='Описание стенда')
    image = models.ImageField(upload_to='media/posts/',
                              blank=True,
                              null=True,
                              verbose_name='Картинка',
                              help_text='Загрузите картинку')

    class Meta:
        ordering = ('title',)
        verbose_name = 'Стенд'
        verbose_name_plural = 'Стенды'

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:100]
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             verbose_name='Комментарий',
                             related_name='comments',
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True,)
    author = models.ForeignKey(User,
                               verbose_name='Автор',
                               related_name='comments',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True,)
    text = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name="follower",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    author = models.ForeignKey(
        User,
        related_name="following",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"


class Task_state(models.Model):
    task_state = models.CharField(max_length=200,
                                  verbose_name='Статус задачи')

    class Meta:
        ordering = ('task_state',)

    def __str__(self) -> str:
        return self.task_state


class Time(models.Model):
    t_start = models.CharField(max_length=200,
                              verbose_name='Время')

    #class Meta:
        #ordering = ('-t_start',)

    def __str__(self) -> str:
        return self.t_start


class Feedback(models.Model):
    text = models.TextField(max_length=1000)
    author = models.ForeignKey(User,
                               verbose_name='Автор',
                               related_name='feedbacks',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True,)
    state = models.ForeignKey('Task_state', # Status
                              blank=True,
                              null=True,
                              on_delete=models.SET_NULL,
                              related_name='fb_states',
                              verbose_name='Статус',
                              default=5,)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(null=True,blank=True,
                                verbose_name='лайки',
                                default=0,)
    dislikes = models.IntegerField(null=True,blank=True,
                                   verbose_name='дизлайки',
                                   default=0,)
    unswer = models.TextField(max_length=1000,
                              blank=True,
                              null=True,)
    image = models.ImageField(upload_to='media/posts/',
                              blank=True,
                              null=True,
                              verbose_name='Картинка',
                              help_text='Загрузите картинку')
    
                                

    class Meta:
        ordering = ['state_id']
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'


class Like(models.Model):
    feedback = models.ForeignKey(Feedback,
                              verbose_name='Отзыв',
                              related_name='f_likes',
                              on_delete=models.CASCADE,
                              blank=True,
                              null=True,)
    user = models.ForeignKey(User,
                               verbose_name='Автор',
                               related_name='u_likes',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True,)

class Dislike(models.Model):
    feedback = models.ForeignKey(Feedback,
                              verbose_name='Отзыв',
                              related_name='f_dislikes',
                              on_delete=models.CASCADE,
                              blank=True,
                              null=True,)
    user = models.ForeignKey(User,
                               verbose_name='Автор',
                               related_name='u_dislikes',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True,)

    
