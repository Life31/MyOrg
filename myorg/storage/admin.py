from django.contrib import admin

from .models import Unit, Th, Event, Type_event, Creator, Ctgry, Place, Si, Stend


class UnitAdmin (admin.ModelAdmin):
    list_display = ('id', 'creator', 'code', 'ctgry', 'place', 'si', 'num', 'comment', 'pub_day', 'author', 'number', 'stend', 'box', 'image')
    search_fields = ('text', )
    list_filter = ('creator', 'ctgry')
    empty_value_display = '-пусто-'


class ThAdmin (admin.ModelAdmin):
    list_display = ('title', 'th', 'day', 'year', 'comment', 'author')
    search_fields = ('title', )
    list_filter = ('day', 'year', 'type_th', 'author', )
    empty_value_display = '-пусто-'


class EventAdmin (admin.ModelAdmin):
    list_display = ('id', 'th_name', 'unit_name', 'event_name', 'num', 'date', 'comment', 'pub_day', 'author')
    search_fields = ('text', )
    list_filter = ('th_name', 'unit_name', 'event_name', 'num', 'date', 'comment', 'pub_day', 'author')
    empty_value_display = '-пусто-'


class Type_eventAdmin (admin.ModelAdmin):
    list_display = ('id', 'name_type')


class CreatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    search_fields = ('text', )
    list_filter = ('id', 'title', 'description')
    empty_value_display = '-пусто-'


class CtgryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    search_fields = ('text', )
    list_filter = ('id', 'title', 'description')
    empty_value_display = '-пусто-'


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    search_fields = ('text', )
    list_filter = ('id', 'title', 'description')
    empty_value_display = '-пусто-'


class SiAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    search_fields = ('text', )
    list_filter = ('title', 'description')
    empty_value_display = '-пусто-'


class StendAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    search_fields = ('text', )
    list_filter = ('id', 'title', 'description')
    empty_value_display = '-пусто-'


admin.site.register(Unit, UnitAdmin)
admin.site.register(Th, ThAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Type_event, Type_eventAdmin)
admin.site.register(Creator, CreatorAdmin)
admin.site.register(Ctgry, CtgryAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Si, SiAdmin)
admin.site.register(Stend, StendAdmin)
