from django.contrib import admin
'''
from .models import Pass
from .models import Car_pass


class PassAdmin(admin.ModelAdmin):
    """Перечисляем поля, которые должны отображаться в админке."""
    list_display = (
        'id', 'pub_date', 'author')
    search_fields = ('author',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class Car_passAdmin(admin.ModelAdmin):
    """Перечисляем поля, которые должны отображаться в админке."""
    list_display = (
        'id', 'pub_date', 'author')
    search_fields = ('author',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Pass, PassAdmin)
admin.site.register(Car_pass, Car_passAdmin)
'''

from .models import Note, Bord, Card

class NoteAdmin(admin.ModelAdmin):
    """Перечисляем поля, которые должны отображаться в админке."""
    list_display = (
        'id', 'text', 'day_start', 'day_update', 'user')
    search_fields = ('author',)
    list_filter = ('day_start',)
    empty_value_display = '-пусто-'


class BordAdmin(admin.ModelAdmin):
    """Перечисляем поля, которые должны отображаться в админке."""
    list_display = (
        'id', 'user', 'guests')
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'


class CardAdmin(admin.ModelAdmin):
    """Перечисляем поля, которые должны отображаться в админке."""
    list_display = (
        'id', 'name', 'bord')
    search_fields = ('name',)
    list_filter = ('bord',)
    empty_value_display = '-пусто-'


admin.site.register(Note, NoteAdmin)
admin.site.register(Bord, BordAdmin)
admin.site.register(Card, CardAdmin)
