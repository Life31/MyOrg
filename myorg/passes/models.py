from enum import unique
from pickle import TRUE
from django.utils import timezone
from django.db import models
import datetime as dt


SPEC_CHOICES = (
    ('Д.А. Мыльников', u'Д.А. Мыльников'),
    ('Л.А. Елагин', u'Л.А. Елагин'),
    ('С.А. Осипенко', u'С.А. Осипенко'),
)


class Pass(models.Model):
    num = models.TextField(verbose_name='Номер', unique=True)
    name = models.TextField(verbose_name='Имя')
    sec_name = models.TextField(verbose_name='Фамилия')
    patro = models.TextField(verbose_name='Отчество')
    where = models.TextField(verbose_name='Откуда')
    day = models.DateTimeField(verbose_name='Дата', default=dt.datetime.now(),)
    pasport = models.TextField(verbose_name='Паспорт', help_text="формат ввода: XXXX XXXXXX")
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)
    doc_type = models.TextField(verbose_name='Документ',
                                default='Паспорт', blank=True, null=True)
    spec = models.TextField(verbose_name='Подписант',
                            default='Д.А. Мыльников',
                            blank=True,
                            null=True,
                            choices=SPEC_CHOICES,)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.TextField(verbose_name='Кто добавил',)
    file = models.FileField(verbose_name='Документ',
                            upload_to='passes/',
                            blank=True,
                            null=True,)

    class Meta:
        ordering = ('-day', '-num',)
        verbose_name = 'Пропуск'
        verbose_name_plural = 'Пропуска'

    def __str__(self) -> str:
        return self.name


class Car_pass(models.Model):
    num = models.TextField(verbose_name='Номер')
    phone = models.TextField(verbose_name='Номер телефона')
    name = models.TextField(verbose_name='Имя')
    sec_name = models.TextField(verbose_name='Фамилия')
    patro = models.TextField(verbose_name='Отчество')
    pasport = models.TextField(verbose_name='Паспорт', help_text="формат ввода: XXXX XXXXXX")
    trans = models.TextField(verbose_name='Провоз на авто')
    auto = models.TextField(verbose_name='Марка и молель авто')
    num_auto = models.TextField(verbose_name='Номер авто')
    stuff = models.TextField(verbose_name='Провозимое имущество')
    quantity = models.TextField(verbose_name='Количество')
    day = models.DateTimeField(blank=True, null=True, 
                               verbose_name='Дата',
                               default=dt.datetime.now(),)
    comment = models.TextField(verbose_name='Комментарий')
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.TextField(verbose_name='Кто добавил',)

    class Meta:
        ordering = ('num',)
        verbose_name = 'Пропуск на машину'
        verbose_name_plural = 'Пропуска на машину'

    def __str__(self) -> str:
        return self.name
