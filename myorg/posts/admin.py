from django.contrib import admin

from .models import Comment, Group, Post, Task_state, Feedback, Like, Dislike


class PostAdmin(admin.ModelAdmin):
    """Перечисляем поля, которые должны отображаться в админке."""
    list_display = (
        'id', 'text', 'pub_date',
        'task_state',
        'group', 'author', 'day',
    )
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
    list_display = ('id', 'title',
                    'slug',
                    'description',)


class Task_stateAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_state', 'state_descr', )


class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'text', 'state', 'author', 'created', 'unswer', 'image',
    )


class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'feedback_id', 'user_id', )


class DislikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'feedback_id', 'user_id', )


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Task_state, Task_stateAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Dislike, DislikeAdmin)
