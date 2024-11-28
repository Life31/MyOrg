from django.contrib import admin

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