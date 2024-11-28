from django.contrib import admin

from .models import Comment, Group, Post, Task_state


class PostAdmin(admin.ModelAdmin):
    """Перечисляем поля, которые должны отображаться в админке."""
    list_display = (
        'id', 'text', 'pub_date',
        'task_state',
        'group', 'author')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    """Перечисляем поля, которые должны отображаться в админке."""
    list_display = ('id', 'author', 'text', 'created')
    search_fields = ('text',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'slug',
                    'description',)


class Task_stateAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_state')


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Task_state, Task_stateAdmin)
