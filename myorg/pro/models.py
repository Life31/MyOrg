from django.db import models
from django.utils import timezone

class Block(models.Model):

    block_type = models.ForeignKey(
        'Type',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='block_type',
        verbose_name='Тип блока',
    )
    number = models.TextField(
        verbose_name='Номер блока',
        unique=True,
    )
    info = models.TextField(
        verbose_name='Информация',
        null=True,
        blank=True,
    )
    block_state = models.ForeignKey(
        'Block_state',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='block_states',
        verbose_name='Статус блока',
    )
    block_state_day = models.DateTimeField(
        verbose_name='Дата последнего статуса',
        null=True,
        blank=True,
        #default=timezone.now,
        )
    on_ready= models.BooleanField(
        null=True,
        blank=True,
        verbose_name='Изготовлен',
    )
    day = models.DateTimeField(
        verbose_name='Дата',
        null=True,
        blank=True,
        #default=timezone.now,
        )

    class Meta:
        ordering = ('block_type', )
        verbose_name = 'Блок'
        verbose_name_plural = 'Блоки'

    def __str__(self) -> str:
        return self.number


class Type(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Тип блока'
    )

    class Meta:
        verbose_name = "Тип блока"
        verbose_name_plural = "Типы блоков"
        ordering = ('id',)

    def __str__(self) -> str:
        return self.name


class Event(models.Model):

    block = models.ForeignKey(
        'Block',
        on_delete=models.CASCADE,
        related_name='block_events',
        verbose_name='Блок',
    )
    event_type = models.ForeignKey(
        'Event_type',
        on_delete=models.CASCADE,
        related_name='block_event',
        verbose_name='Тип события',
    )
    description = models.TextField(
        verbose_name='Описание события',
        null=True,
        blank=True,
    )
    day = models.DateTimeField(
        verbose_name='Дата',
        null=True,
        blank=True,
        #default=timezone.now,
        )

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"
        ordering = ('id',)


class Event_type(models.Model):
    event_type = models.CharField(
        max_length=200,
        verbose_name='Тип события'
    )

    class Meta:
        verbose_name = "Тип события"
        verbose_name_plural = "Типы событий"
        ordering = ('id',)

    def __str__(self) -> str:
        return self.event_type


class Block_state(models.Model):
    block_state = models.CharField(
        max_length=200,
        verbose_name='Статус'
    )

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ('id',)

    def __str__(self) -> str:
        return self.block_state