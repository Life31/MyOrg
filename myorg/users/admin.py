from django.contrib import admin
from .models import User_info


class User_infoAdmin(admin.ModelAdmin):
    """Информация о пользователях"""
    list_display = (
        'user', 'boss', 'otd_number',
        'reqs_access',
        'pass_access',
        'stor_access',
        'task_access',
        'corr_access',
        'conf_access',
        'user_access',
    )
    search_fields = ('user', )


admin.site.register(User_info, User_infoAdmin)
