from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
# from calendar import monthrange

# from pytils.translit import slugify
# import datetime as dt

User = get_user_model()


class Unit(models.Model):
    name = models.TextField(verbose_name='Наименование',)
    creator = models.ForeignKey('Creator',
                                on_delete=models.SET_NULL,
                                blank=True,
                                null=True,
                                related_name='creators',
                                verbose_name='Производитель',)
    code = models.TextField(verbose_name='Обозначение',)
    ctgry = models.ForeignKey('Ctgry',
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True,
                              related_name='ctgrys',
                              verbose_name='Категория',)
    place = models.ForeignKey('Place',
                              on_delete=models.SET_NULL,
                              blank=True,
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
    number = models.TextField(verbose_name='Номер учетный',
                              blank=True, null=True,)
    stend = models.ForeignKey('Stend',
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True,
                              default = 1,
                              related_name='stends',
                              verbose_name='Стенд',)
    box = models.TextField(verbose_name='Номер коробки',
                           blank=True, null=True,)
    

    class Meta:
        ordering = ('name', )
        verbose_name = 'Учетная еденица'
        verbose_name_plural = 'Учетные еденицы'

    def __str__(self) -> str:
        return self.name[:25]


class Th(models.Model):
    name = models.ForeignKey('Unit',
                             on_delete=models.SET_NULL,
                             blank=True,
                             null=True,
                             related_name='units',
                             verbose_name='Учетная единица',)
    title = models.TextField(verbose_name='Номер накладной',)
    num = models.TextField(verbose_name='Количество',)
    money = models.TextField(verbose_name='Стоимость',blank=True,
                             null=True,)
    cz = models.FileField(verbose_name='Служебная записка',
                          upload_to='storage/',
                          blank=True,
                          null=True,)
    th = models.FileField(verbose_name='Накладная',
                          upload_to='storage/',
                          blank=True,
                          null=True,)
    day = models.DateTimeField(blank=True, null=True,
                               verbose_name='Дата',
                               default=timezone.now,
                               #default=dt.datetime.now().date(),
                               help_text="формат ввода: YYYY-mm-dd")
    comment = models.TextField(verbose_name='Комментарий',)
    pub_day = models.TextField(verbose_name='Дата',
                               default=timezone.now().date(),)
    author = models.TextField(verbose_name='Кто добавил',)

    class Meta:
        ordering = ('-day', )
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self) -> str:
        return self.text[:15]


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
        verbose_name = 'Место хранения'
        verbose_name_plural = 'Места хранения'

    def __str__(self) -> str:
        return self.title
