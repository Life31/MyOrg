from django.contrib import admin

from .models import Unit, Include, Config, Number, Query, Change


class UnitAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'unit_type', 'creator', 'serial_n',
        'part_n', 'doc', 'pub_date', 'author', )
    search_fields = ('unit_type',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'

class IncludeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit', )
    search_fields = ('name',)
    list_filter = ('unit',)
    empty_value_display = '-пусто-'


class ConfigAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'unit', 'include_name', 'part_n',
        'other_info', 'descr', 'doc', 'number',
        'pub_date', 'author', )
    search_fields = ('unit',)
    list_filter = ('number',)
    empty_value_display = '-пусто-'

class NumberAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', )
    search_fields = ('number',)
    list_filter = ('number',)
    empty_value_display = '-пусто-'


class QueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'state', 'author', 'pub_date', )
    search_fields = ('number',)
    list_filter = ('number',)
    empty_value_display = '-пусто-'


class ChangeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'number', 'unit', 'include_name',
        'part_n', 'other_info', 'descr', 'doc',
        'pub_date', 'author', 'state', )
    search_fields = ('number',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Change, ChangeAdmin)
admin.site.register(Query, QueryAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Include, IncludeAdmin)
admin.site.register(Config, ConfigAdmin)
admin.site.register(Number, NumberAdmin)
