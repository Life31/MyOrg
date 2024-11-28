from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models
import transliterate

User = get_user_model()


def rename_file(instance, filename):
    try:
        filename = transliterate.translit(filename, reversed=True)
    except:
        filename = filename
    return '/'.join(['media', 'task', filename])

User = get_user_model()


class Task(models.Model):

    master = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='out_tasks',
        verbose_name='Автор',
    )
    slave = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='in_tasks',
        verbose_name='Исполнитель',
    )
    text = models.TextField(
        verbose_name='Текст задачи',
    )
    state = models.ForeignKey(
        'Task_state',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='states',
        verbose_name='Статус',
        default=1,
    )
    persent = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='%',
    )
    image = models.ImageField(
        upload_to=rename_file,
        blank=True,
        null=True,
        verbose_name='Картинка',
        help_text='Загрузите картинку',
    )
    file = models.FileField(
        verbose_name='Документ',
        upload_to=rename_file,
        blank=True,
        null=True,
    )
    day_start = models.DateTimeField(
        blank=True, null=True,
        verbose_name='Дата начала',
        default=timezone.now,
    )
    day_end = models.DateTimeField(
        blank=True, null=True,
        verbose_name='Назначенная дата завершения',
    )
    result = models.TextField(
        blank=True, null=True,
        verbose_name='Результат'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )
    ###
    card = models.ForeignKey(
        'Card',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='cards',
        verbose_name='Карточка',
    )
    bord_link = models.ForeignKey(
        'Bord',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='task_bord_link',
        verbose_name='ссылка на доску задачи',
    )
    same_id = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='id',
    )
    day_real_end = models.DateTimeField(
        blank=True, null=True,
        verbose_name='Дата фактического завершения',
    )
    new = models.BooleanField(
        blank=True,
        null=True,
        default=True,
        verbose_name='Новая задача или нет',
    )
    bord = models.ForeignKey(
        'Bord',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='task_bord',
        verbose_name='принадлежность к доске',
    )

    class Meta:
        ordering = ('master',)
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
    '''
    def __str__(self) -> str:
        return self.name
    '''
    def save(self, *args, **kwargs):
        self.same_id = self.pk
        super().save(*args, **kwargs)


class Task_state(models.Model):
    task_state = models.CharField(
        max_length=200,
        verbose_name='Статус задачи',
    )

    class Meta:
        ordering = ('task_state',)
        verbose_name = "Статус задачи или обращения"
        verbose_name_plural = "Статусы задач и обращений"

    def __str__(self) -> str:
        return self.task_state


class Bord(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Доска',
    )
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='user_bords',
        verbose_name='Пользователь',
    )
    guests = models.TextField(
        blank=True, null=True,
        verbose_name='Гости',
        default="",
    )

    class Meta:
        ordering = ('name',)
        verbose_name = "Доска"
        verbose_name_plural = "Доски"

    def __str__(self) -> str:
        return self.name


class Card(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Карточка',
    )
    bord = models.ForeignKey(
        'Bord',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='bord_cards',
        verbose_name='Доска',
    )

    class Meta:

        verbose_name = "Карточка"
        verbose_name_plural = "Карточки"

    def __str__(self) -> str:
        return self.name


class Note(models.Model):

    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='user_notes',
        verbose_name='Автор',
    )
    text = models.TextField(
        blank=True, null=True,
        verbose_name='Заметка',
        default="Новая заметка",
    )
    day_start = models.DateTimeField(
        blank=True, null=True,
        verbose_name='Дата создания',
        default=timezone.now,
    )
    day_update = models.DateTimeField(
        blank=True, null=True,
        verbose_name='Дата последнего изменения',
        default=timezone.now,
    )
    same_id = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='id',
    )

    class Meta:
        ordering = ('-day_update',)
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"

    def __str__(self) -> str:
        if len(self.text) > 25:
            return self.text[:25] + '...'
        return self.text
