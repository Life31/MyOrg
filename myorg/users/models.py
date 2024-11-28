from django.contrib.auth import get_user_model
from django.db import models
from posts.models import Unit
import datetime as dt
User = get_user_model()


class User_info(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_info',
        verbose_name='Пользователь',
    )
    position = models.ForeignKey(
        'Position',
        on_delete=models.CASCADE,
        related_name='position_info',
        verbose_name='должность',
        null=True,
        blank=True,
    )
    boss = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='boss_info',
        verbose_name='Руководитель',
    )
    otd_number = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Номер отдела',
    )
    reqs_access = models.BooleanField(
        null=True,
        blank=True,
        default=True,
        verbose_name='Доступ к заявкам',
    )
    pass_access = models.BooleanField(
        null=True,
        blank=True,
        default=False,
        verbose_name='Доступ к пропускам',
    )
    stor_access = models.BooleanField(
        null=True,
        blank=True,
        default=False,
        verbose_name='Доступ к складу',
    )
    task_access = models.BooleanField(
        null=True,
        blank=True,
        default=False,
        verbose_name='Доступ к задачам',
    )
    corr_access = models.BooleanField(
        null=True,
        blank=True,
        default=False,
        verbose_name='Доступ к корреспонденции',
    )
    conf_access = models.BooleanField(
        null=True,
        blank=True,
        default=False,
        verbose_name='Доступ к конфигурации',
    )
    user_access = models.BooleanField(
        null=True,
        blank=True,
        default=False,
        verbose_name='Доступ к сотрудникам',
    )
    vacs_access = models.BooleanField(
        null=True,
        blank=True,
        default=False,
        verbose_name='Доступ к отпускам',
    )
    test_access = models.BooleanField(
        null=True,
        blank=True,
        default=False,
        verbose_name='Доступ к тестам',
    )
    bibl_access = models.BooleanField(
        null=True,
        blank=True,
        default=False,
        verbose_name='Доступ к библиотеке',
    )
    news_access = models.BooleanField(
        null=True,
        blank=True,
        default=True,
        verbose_name='Доступ к новостям',
    )
    mess_access = models.BooleanField(
        null=True,
        blank=True,
        default=False,
        verbose_name='Доступ к мессенджеру',
    )
    phone_number = models.TextField(
        verbose_name='Номер телефона',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('boss', )
        verbose_name = 'Информация о пользователе'
        verbose_name_plural = 'Информация о пользователях'


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


class Position(models.Model):
    position = models.CharField(max_length=200, verbose_name='должность')

    class Meta:
        ordering = ('position',)
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self) -> str:
        return self.position


class Log(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_logs',
        verbose_name='Пользователь',
        blank=True,
        null=True,
    )
    day = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата',
        default=dt.datetime.now(),
    )
    event = models.TextField(
        verbose_name='Событие',
        blank=True,
        null=True,
    )
    res = models.TextField(
        verbose_name='Ресурс',
        blank=True,
        null=True,
    )
    before = models.TextField(
        verbose_name='До изменений',
        blank=True,
        null=True,
    )
    after = models.TextField(
        verbose_name='После изменений',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('-day',)
        verbose_name = 'Запись'


class Vacation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_vacations',
        verbose_name='Пользователь',
        blank=True,
        null=True,
    )
    day_start = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата начала',
    )
    day_end = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата окончания',
    )
    how_long = models.TextField(
        verbose_name='Всего дней',
        blank=True,
        null=True,
    )
    year = models.TextField(
        verbose_name='Период',
        blank=True,
        null=True,
    )
    can_redact = models.BooleanField(
        verbose_name='Возможность редактировать',
        blank=True,
        null=True,
        default=True,
    )

    class Meta:
        ordering = ('user', 'day_start', )
        verbose_name = 'Отпуск'

    def save(self, *args, **kwargs):
        self.year = str(self.day_start.year)
        super().save(*args, **kwargs) 


class User_widgets(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_widgets',
        verbose_name='Пользователь',
        blank=True,
        null=True,
    )
    reqs = models.BooleanField(
        verbose_name='Заявки на испытания',
        blank=True,
        null=True,
        default=False,
    )
    reqs_open = models.BooleanField(
        verbose_name='Заявки на испытания открыт',
        blank=True,
        null=True,
        default=False,
    )
    vacs = models.BooleanField(
        verbose_name='Отпуска',
        blank=True,
        null=True,
        default=False,
    )
    vacs_open = models.BooleanField(
        verbose_name='Отпуска открыт',
        blank=True,
        null=True,
        default=False,
    )
    test = models.BooleanField(
        verbose_name='Тесты',
        blank=True,
        null=True,
        default=False,
    )
    test_open = models.BooleanField(
        verbose_name='Тесты открыт',
        blank=True,
        null=True,
        default=False,
    )
    corr = models.BooleanField(
        verbose_name='Корреспонденция',
        blank=True,
        null=True,
        default=False,
    )
    corr_open = models.BooleanField(
        verbose_name='Корреспонденция открыт',
        blank=True,
        null=True,
        default=False,
    )
    task = models.BooleanField(
        verbose_name='Задачи',
        blank=True,
        null=True,
        default=False,
    )
    task_open = models.BooleanField(
        verbose_name='Задачи открыт',
        blank=True,
        null=True,
        default=False,
    )
    bibl = models.BooleanField(
        verbose_name='Библиотека',
        blank=True,
        null=True,
        default=False,
    )
    bibl_open = models.BooleanField(
        verbose_name='Библиотека открыта',
        blank=True,
        null=True,
        default=False,
    )
    stor = models.BooleanField(
        verbose_name='Склад',
        blank=True,
        null=True,
        default=False,
    )
    stor_open = models.BooleanField(
        verbose_name='Склад открыт',
        blank=True,
        null=True,
        default=False,
    )
    news = models.BooleanField(
        verbose_name='Новости',
        blank=True,
        null=True,
        default=True,
    )
    news_open = models.BooleanField(
        verbose_name='Новости открыт',
        blank=True,
        null=True,
        default=False,
    )
    mess = models.BooleanField(
        verbose_name='Мессенджер',
        blank=True,
        null=True,
        default=False,
    )
    mess_open = models.BooleanField(
        verbose_name='Мессенджер открыт',
        blank=True,
        null=True,
        default=False,
    )
    users = models.BooleanField(
        verbose_name='Сотрудники',
        blank=True,
        null=True,
        default=False,
    )
    users_open = models.BooleanField(
        verbose_name='Сотрудники открыт',
        blank=True,
        null=True,
        default=False,
    )
    notes = models.BooleanField(
        verbose_name='Заметки',
        blank=True,
        null=True,
        default=True,
    )
    notes_open = models.BooleanField(
        verbose_name='Заметки открыт',
        blank=True,
        null=True,
        default=False,
    )
    calc = models.BooleanField(
        verbose_name='Калькулятор',
        blank=True,
        null=True,
        default=True,
    )
    calc_open = models.BooleanField(
        verbose_name='Калькулятор открыт',
        blank=True,
        null=True,
        default=False,
    )
    widgets_order = models.TextField(
        verbose_name='Порядок виджетов',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('user', )
        verbose_name = 'Доступ к виджетам'


class Message(models.Model):
    user_one = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_one_mess',
        verbose_name='Первый пользователь',
        blank=True,
        null=True,
    )
    user_two = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_two_mess',
        verbose_name='Второй пользователь',
        blank=True,
        null=True,
    )
    witch_write = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_witch_write',
        verbose_name='Пользователь который написал',
        blank=True,
        null=True,
    )
    text = models.TextField(
        verbose_name='Номер заявки',
        blank=True,
        null=True,
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата',
    )
    '''
    image = models.ImageField(
        upload_to='media/posts/',
        blank=True,
        null=True,
        verbose_name='Картинка',
        help_text='Загрузите картинку',
    )
    file = models.FileField(
        verbose_name='Документ', # Documents
        upload_to='files/',
        blank=True,
        null=True,
    )'''
    readed = models.BooleanField(
        verbose_name='Прочитанно',
        blank=True,
        null=True,
        default=False,
    )

    class Meta:
        ordering = ('pub_date', )
        verbose_name = 'Переписка'
