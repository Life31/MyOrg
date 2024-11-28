from django.contrib import admin

from .models import Corresp, In_out, Type, Who



class CorrespAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'number',
        'in_out',
        'company',
        'from_who',
        'to',
        'day',
        'comment')
    search_fields = ('number',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class In_outAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'dirr',)


class TypeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cor_type',)


class WhoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'who',)

admin.site.register(Corresp, CorrespAdmin)
admin.site.register(In_out, In_outAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Who, WhoAdmin)
