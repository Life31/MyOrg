from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
# from calendar import monthrange
from django.conf import settings
# from pytils.translit import slugify
import datetime as dt
import os
import transliterate

User = get_user_model()

def get_path(instance, filename):
    return os.path.join(
        'storage/',
        str(instance.year)
        +'/'+
        str(instance.type_th),
        filename
        )


def rename_file(instance, filename):
    try:
        filename = transliterate.translit(filename, reversed=True)
    except:
        filename = filename
    return '/'.join(['media', 'storage', filename])


class Unit(models.Model):
    name = models.TextField(verbose_name='Наименование',)
    image = models.ImageField(upload_to=rename_file,
                              blank=True,
                              null=True,
                              verbose_name='Картинка',
                              help_text='Загрузите картинку')
    creator = models.ForeignKey('Creator',
                                on_delete=models.SET_NULL,
                                #blank=True,
                                null=True,
                                related_name='creators',
                                verbose_name='Производитель',)
    code = models.TextField(verbose_name='Обозначение',)
    ctgry = models.ForeignKey('Ctgry',
                              on_delete=models.SET_NULL,
                              #blank=True,
                              null=True,
                              related_name='ctgrys',
                              verbose_name='Категория',)
    place = models.ForeignKey('Place',
                              on_delete=models.SET_NULL,
                              #blank=True,
                              null=True,
                              related_name='places',
                              verbose_name='Место хранения',)

    si = models.ForeignKey('Si',
                           on_delete=models.SET_NULL,
                           blank=True,
                           null=True,
                           related_name='sis',
                           verbose_name='Еденицы измерения',)
    num = models.TextField(verbose_name='Количество',)
    comment = models.TextField(verbose_name='Комментарий',
                               blank=True, null=True,)
    pub_day = models.TextField(verbose_name='Дата',
                               default=timezone.now().date(),)
    author = models.TextField(verbose_name='Кто добавил',)
    number = models.IntegerField(verbose_name='Номер учетный',
                              blank=True, null=True,)
    stend = models.ForeignKey('Stend',
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True,
                              default = 10,
                              related_name='stends',
                              verbose_name='Стенд',)
    box = models.TextField(verbose_name='Номер коробки',
                           blank=True, null=True,)
    pack = models.TextField(verbose_name='Место хранения упаковки',
                           blank=True, null=True,)
    acctual = models.BooleanField(
        default=1,
        verbose_name='Данные актуальны',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('-number', )
        verbose_name = 'Учетная еденица'
        verbose_name_plural = 'Учетные еденицы'

    def __str__(self) -> str:
        return self.name[:25]


TYPE_CHOICES = (
    ('Входящие', u'Входящие'),
    ('Исходящие', u'Исходящие'),
)
NOW = dt.datetime.now().year
YEAR_CHOICES = (
    (str(int(NOW) - 5), str(int(NOW) - 5)),
    (str(int(NOW) - 4), str(int(NOW) - 4)),
    (str(int(NOW) - 3), str(int(NOW) - 3)),
    (str(int(NOW) - 2), str(int(NOW) - 2)),
    (str(int(NOW) - 1), str(int(NOW) - 1)),
    (str(NOW), str(NOW)),
    (str(int(NOW) + 1), str(int(NOW) + 1)),
)


class Th(models.Model):
    '''Класс товарных накладных'''
    title = models.TextField(verbose_name='Номер накладной', blank=True,
                             null=True,)
    type_th = models.TextField(verbose_name='Вх. / Исх.', blank=True,
                             null=True, choices=TYPE_CHOICES)
    year = models.TextField(verbose_name='Год',blank=True,
                             null=True, choices=YEAR_CHOICES)
    th = models.FileField(verbose_name='Накладная',
                          upload_to=get_path,#'storage/',
                          blank=True,
                          null=True,)
    day = models.DateTimeField(blank=True, null=True,
                               verbose_name='Дата',
                               default=timezone.now,)
                               #default=dt.datetime.now().date(),)
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True,)
    pub_day = models.TextField(
        verbose_name='Дата',
        default=timezone.now().date(),
    )
    author = models.TextField(verbose_name='Кто добавил',)
    unit_number = models.TextField(
        verbose_name='номер уч. ед.',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('-day', )
        verbose_name = 'Накладная'
        verbose_name_plural = 'Накладные'

    def __str__(self) -> str:
        return self.title[:15]

class Event(models.Model):
    th_name = models.ForeignKey('Th',
                             on_delete=models.SET_NULL,
                             blank=True,
                             null=True,
                             related_name='ths',
                             verbose_name='Накладная',)
    unit_name = models.ForeignKey('Unit',
                             on_delete=models.SET_NULL,
                             blank=True,
                             null=True,
                             related_name='units',
                             verbose_name='Учетная единица',)
    event_name = models.ForeignKey('Type_event',
                             on_delete=models.SET_NULL,
                             blank=True,
                             null=True,
                             related_name='events',
                             verbose_name='Событие')
    num = models.TextField(verbose_name='Количество', blank=True, null=True, )
    date = models.DateTimeField(blank=True, null=True,
                               verbose_name='Дата',
                               default=timezone.now,
                               #default=dt.datetime.now().date(),
                               help_text="формат ввода: YYYY-mm-dd")
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True,)
    pub_day = models.TextField(verbose_name='Дата',
                               default=timezone.now().date(),)
    author = models.TextField(verbose_name='Кто добавил',)

    class Meta:
        ordering = ('-date', )
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self) -> str:
        return self.event_name[:15]


class Type_event(models.Model):
    name_type = models.TextField(verbose_name='Тип')

    class Meta:
        verbose_name = 'Тип события'
        verbose_name_plural = 'Типы событий'

    def __str__(self) -> str:
        return self.name_type[:15]
    
class Creator(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Производитель')
    description = models.CharField(blank=True,
                                   null=True,
                                   max_length=200,
                                   verbose_name='Описание')

    class Meta:
        ordering = ('title',)
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self) -> str:
        return self.title


class Ctgry(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Категория')
    description = models.CharField(blank=True,
                                   null=True,
                                   max_length=200,
                                   verbose_name='Описание')
    class Meta:
        ordering = ('title',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title


class Place(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Место хранения')
    description = models.CharField(blank=True,
                                   null=True,
                                   max_length=200,
                                   verbose_name='Описание')

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Место хранения'
        verbose_name_plural = 'Места хранения'

    def __str__(self) -> str:
        return self.title


class Si(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Еденица измерения')
    description = models.CharField(blank=True,
                                   null=True,
                                   max_length=200,
                                   verbose_name='Описание')
    
    class Meta:
        ordering = ('title',)
        verbose_name = 'Еденицы измерения'
        verbose_name_plural = 'Еденицы измерения'

    def __str__(self) -> str:
        return self.title

class Stend(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Стенд')
    description = models.CharField(blank=True,
                                   null=True,
                                   max_length=200,
                                   verbose_name='Описание')

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Стенд'
        verbose_name_plural = 'Стенды'

    def __str__(self) -> str:
        return self.title


class Tag(models.Model):
    tag = models.CharField(max_length=200, verbose_name='Тег')

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.tag


class Th_tags(models.Model):

    tag = models.ForeignKey('Tag',
                             on_delete=models.SET_NULL,
                             related_name='th_tags',
                             verbose_name='Таг',
                             blank=True,
                             null=True,)
    th = models.ForeignKey('Th',
                             on_delete=models.SET_NULL,
                             related_name='ths_tag',
                             verbose_name='Накладная',
                             blank=True,
                             null=True,)
    class Meta:
        ordering = ('tag',)
        verbose_name = 'Запись типа:Тег - накладная'
        verbose_name_plural = 'Записи типа:Тег - накладная'

    def __str__(self) -> str:
        return self.tag


class User_units(models.Model):

    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             related_name='user_units',
                             verbose_name='Пользователь',
                             blank=True,
                             null=True,)
    unit = models.ForeignKey('Unit',
                             on_delete=models.SET_NULL,
                             related_name='unit_users',
                             verbose_name='Уч. единица',
                             blank=True,
                             null=True,)
    class Meta:
        ordering = ('user',)
        verbose_name = 'Запись типа: Пользователь - уч. единица'
        verbose_name_plural = 'Записи типа: Пользователь - уч. единица'
