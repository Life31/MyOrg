from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from calendar import monthrange

import datetime as dt
User = get_user_model()
#---------------------------------------------------------new
class Unit(models.Model):
    unit_type = models.TextField(verbose_name='Тип блока', unique=True, )
    position = models.TextField(verbose_name='Позация', blank=True, null=True, )
    creator = models.TextField(verbose_name='Производитель',
                               blank=True, null=True,)
    serial_n = models.TextField(verbose_name='S/N', blank=True, null=True, )
    part_n = models.TextField(verbose_name='P/N', blank=True, null=True, )
    descr = models.TextField(verbose_name='Примечание', blank=True, null=True, )
    doc = models.FileField(verbose_name='Документ', 
                            upload_to='config/монтаж/',
                            blank=True,
                            null=True,)
    pos_on_storage = models.IntegerField(verbose_name='Позация на кладе', blank=True, null=True, )
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='units',
                               verbose_name='Автор',)

    class Meta:
        ordering = ('id', )
        verbose_name = 'Блок'
        verbose_name_plural = 'Блоки'

    def __str__(self) -> str:
        return str(self.unit_type)


class Configuration(models.Model):
    unit = models.ForeignKey('Unit',
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='c_units',
                              verbose_name='Блок')
    parametr = models.TextField(verbose_name='Параметр', )
    part_n = models.TextField(verbose_name='P/N', )
    other_info = models.TextField(verbose_name='Проч. идент. конф.',
                                  blank=True, null=True,)
    descr = models.TextField(verbose_name='Примечание', )
    doc = models.FileField(verbose_name='Документ', 
                            upload_to='config/доводочные работы/',
                            blank=True,
                            null=True,)
    number = models.ForeignKey('Number',
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='c_numbers',
                              verbose_name='Номер конфигурации')

    class Meta:
        ordering = ('number', 'unit')
        verbose_name = 'Запись о конфигурации'
        verbose_name_plural = 'Записи о конфигурации'

    def __str__(self) -> str:
        return str(self.parametr)


class Changes(models.Model):
    unit = models.ForeignKey('Unit',
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='chs_units',
                              verbose_name='Блок')
    parametr = models.TextField(verbose_name='Параметр', )
    part_n = models.TextField(verbose_name='P/N', )
    other_info = models.TextField(verbose_name='Проч. идент. конф.',
                                  blank=True, null=True,)
    descr = models.TextField(verbose_name='Примечание', )
    doc = models.FileField(verbose_name='Документ', 
                            upload_to='config/доводочные работы/',
                            blank=True,
                            null=True,)
    number = models.ForeignKey('Number',
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='chs_numbers',
                              verbose_name='Номер конфигурации')

    class Meta:
        ordering = ('number', 'unit', 'id')
        verbose_name = 'Запись о изменении'
        verbose_name_plural = 'Записи о изменениях'

    def __str__(self) -> str:
        return str(self.parametr)


class Changes_confirm(models.Model):
    unit = models.ForeignKey('Unit',
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='c_chs_units',
                              verbose_name='Блок')
    parametr = models.TextField(verbose_name='Параметр', )
    part_n = models.TextField(verbose_name='P/N', )
    other_info = models.TextField(verbose_name='Проч. идент. конф.',
                                  blank=True, null=True,)
    descr = models.TextField(verbose_name='Примечание', )
    doc = models.FileField(verbose_name='Документ', 
                            upload_to='config/доводочные работы/',
                            blank=True,
                            null=True,)
    number = models.ForeignKey('Number',
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='c_chs_numbers',
                              verbose_name='Номер конфигурации')

    class Meta:
        ordering = ('number', 'unit', '-id')
        verbose_name = 'Подтвержденная запись о изменении'
        verbose_name_plural = 'Подтвержденные записи о изменениях'

    def __str__(self) -> str:
        return str(self.parametr)

#---------------------------------------------------------new
class Include(models.Model):
    name = models.TextField(verbose_name='Влож. эл. конф.', )
    unit = models.ForeignKey('Unit',
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='includes',
                              verbose_name='Блок')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Влож. эл. конф.'
        verbose_name_plural = 'Влож. эл. конф.'

    def __str__(self) -> str:
        return str(self.name)


class Config(models.Model):
    unit = models.ForeignKey('Unit',
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='units',
                              verbose_name='Блок')
    include_name = models.ForeignKey('Include',
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='includes',
                              verbose_name='Влож. эл. конф.')
    part_n = models.TextField(verbose_name='P/N', )
    other_info = models.TextField(verbose_name='Проч. идент. конф.',
                                  blank=True, null=True,)
    descr = models.TextField(verbose_name='Примечание', )
    doc = models.FileField(verbose_name='Документ', 
                            upload_to='config/доводочные работы/',
                            blank=True,
                            null=True,)
    number = models.ForeignKey('Number',
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='numbers',
                              verbose_name='Номер конфигурации')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='configs',
                               verbose_name='Автор',)

    class Meta:
        ordering = ('number', )
        verbose_name = 'Запись о конфигурации'
        verbose_name_plural = 'Записи о конфигурации'

    def __str__(self) -> str:
        return str(self.part_n)


class Number(models.Model):
    number = models.TextField(verbose_name='номер конфигурации', )

    class Meta:
        ordering = ('number',)
        verbose_name = 'Номер конфигурации'
        verbose_name_plural = 'Номера конфигурации'

    def __str__(self) -> str:
        return str(self.number)


class Query(models.Model):
    number = models.ForeignKey(Number,
                               on_delete=models.CASCADE,
                               related_name='q_numbers',
                               verbose_name='Текущий номер конфигурации',)
    state = models.TextField(verbose_name='Статус', )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='users',
                               verbose_name='Автор',)
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата')

    class Meta:
        ordering = ('number',)
        verbose_name = 'Запрос на изменение конфигурации'
        verbose_name_plural = 'Запросы на изменение конфигурации'

    def __str__(self) -> str:
        return str(self.id)


class Change(models.Model):
    number = models.ForeignKey(Query,
                               on_delete=models.CASCADE,
                               related_name='changes',
                               verbose_name='Номер запроса',)
    unit = models.ForeignKey('Unit',
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='ch_units',
                              verbose_name='Блок')
    include_name = models.ForeignKey('Include',
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='ch_includes',
                              verbose_name='Влож. эл. конф.')
    part_n = models.TextField(verbose_name='P/N', )
    other_info = models.TextField(verbose_name='Проч. идент. конф.',
                                  blank=True, null=True,)
    descr = models.TextField(verbose_name='Примечание', )
    doc = models.FileField(verbose_name='Документ', 
                            upload_to='config/доводочные работы/',
                            blank=True,
                            null=True,)
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='ch_configs',
                               verbose_name='Автор',)
    state = models.TextField(verbose_name='Статус', )#add, del, fix

    class Meta:
        ordering = ('number',)
        verbose_name = 'изменение конфигурации'
        verbose_name_plural = 'изменения конфигурации'

    def __str__(self) -> str:
        return str(self.number)
