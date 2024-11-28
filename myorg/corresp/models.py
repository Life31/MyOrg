from django.utils import timezone
from django.db import models
import os
import transliterate

def get_path(instance, filename):
    return transliterate.translit(os.path.join(
        'correspondence/',
        str(instance.cor_type)
        +'/'+
        str(instance.in_out),
        filename
    ), reversed=True)


class Corresp(models.Model):
    cor_type = models.ForeignKey('Type',
                                 blank=True,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 related_name='cor_types',
                                 verbose_name='Тип',
                                 default=1,)
    number = models.TextField(verbose_name='Номер')
    in_out = models.ForeignKey('In_out',
                               #blank=True,
                               null=True,
                               on_delete=models.SET_NULL,
                               related_name='in_out_dirr',
                               verbose_name='Вх/Исх',
                               default=0,)
    company = models.TextField(
        verbose_name='Компания',
        blank=True,
        null=True,
    )
    from_who = models.ForeignKey('Who',
                                 blank=True,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 related_name='from_whos',
                                 verbose_name='От кого',
                                 default=1,)
    to = models.ForeignKey('Who',
                           blank=True,
                           null=True,
                           on_delete=models.SET_NULL,
                           related_name='to_whos',
                           verbose_name='Кому',
                           default=1,)
    day = models.DateTimeField(blank=True, null=True,
                               verbose_name='Дата',
                               default=timezone.now,
                               help_text="формат ввода: YYYY-mm-dd")
    comment = models.TextField(verbose_name='Описание')
    pub_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    author = models.TextField(verbose_name='Кто добавил', blank=True, null=True, )
    file = models.FileField(verbose_name='Документ',
                            upload_to=get_path,
                            blank=True,
                            null=True,)
    tag = models.TextField(
        verbose_name='Тэг',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('-day',)
        verbose_name = 'Корреспонденция'
        verbose_name_plural = 'Корреспонденция'

    def __str__(self) -> str:
        return self.number


class In_out(models.Model):
    dirr = models.CharField(max_length=50,
                            verbose_name='Направление')

    class Meta:
        ordering = ('dirr',)

    def __str__(self) -> str:
        return self.dirr


class Type(models.Model):
    cor_type = models.CharField(max_length=50,
                            verbose_name='Тип')

    class Meta:
        ordering = ('cor_type',)

    def __str__(self) -> str:
        return self.cor_type

class Who(models.Model):
    who = models.CharField(max_length=200,
                           verbose_name='автор/адресант')

    class Meta:
        ordering = ('who',)

    def __str__(self) -> str:
        return self.who
