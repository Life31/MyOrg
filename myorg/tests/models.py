from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Test(models.Model):
    name = models.TextField(verbose_name='Тест')

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self) -> str:
        return self.name[:30]


class Question(models.Model):
    quest = models.TextField(verbose_name='Вопрос')
    right_unswer = models.TextField(verbose_name='Правилный ответ')
    unswer_2 = models.TextField(verbose_name='ответ 2')
    unswer_3 = models.TextField(verbose_name='ответ 3')
    unswer_4 = models.TextField(verbose_name='ответ 4')
    test = models.ForeignKey('Test',
                           on_delete=models.SET_NULL,
                           blank=True,
                           null=True,
                           related_name='questions',
                           verbose_name='Тест',)
    same_id = models.IntegerField(verbose_name='id вопроса', blank=True,
                           null=True,)
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self) -> str:
        return self.quest[:30]

    def save(self, *args, **kwargs):

        self.same_id = self.pk
        super().save(*args, **kwargs)

class Unswers(models.Model):
    user = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='user_unswers',
                               verbose_name='Пользователь',)

    test = models.ForeignKey('Test',
                           on_delete=models.SET_NULL,
                           blank=True,
                           null=True,
                           related_name='unswers',
                           verbose_name='Тест',)
    unswer_1 = models.TextField(verbose_name='ответ 1', blank=True, null=True,)
    unswer_2 = models.TextField(verbose_name='ответ 2', blank=True, null=True,)
    unswer_3 = models.TextField(verbose_name='ответ 3', blank=True, null=True,)
    unswer_4 = models.TextField(verbose_name='ответ 4', blank=True, null=True,)
    unswer_5 = models.TextField(verbose_name='ответ 5', blank=True, null=True,)
    unswer_6 = models.TextField(verbose_name='ответ 6', blank=True, null=True,)
    unswer_7 = models.TextField(verbose_name='ответ 7', blank=True, null=True,)
    unswer_8 = models.TextField(verbose_name='ответ 8', blank=True, null=True,)
    unswer_9 = models.TextField(verbose_name='ответ 9', blank=True, null=True,)
    unswer_10 = models.TextField(verbose_name='ответ 10', blank=True, null=True,)
    unswer_11 = models.TextField(verbose_name='ответ 11', blank=True, null=True,)
    unswer_12 = models.TextField(verbose_name='ответ 12', blank=True, null=True,)
    unswer_13 = models.TextField(verbose_name='ответ 13', blank=True, null=True,)
    unswer_14 = models.TextField(verbose_name='ответ 14', blank=True, null=True,)
    unswer_15 = models.TextField(verbose_name='ответ 15', blank=True, null=True,)
    unswer_16 = models.TextField(verbose_name='ответ 16', blank=True, null=True,)
    unswer_17 = models.TextField(verbose_name='ответ 17', blank=True, null=True,)
    unswer_18 = models.TextField(verbose_name='ответ 18', blank=True, null=True,)
    unswer_19 = models.TextField(verbose_name='ответ 19', blank=True, null=True,)
    unswer_20 = models.TextField(verbose_name='ответ 20', blank=True, null=True,)


    class Meta:
        verbose_name = 'Ответы'
        verbose_name_plural = 'Ответы'

    def __str__(self) -> str:
        return self.test[:30]