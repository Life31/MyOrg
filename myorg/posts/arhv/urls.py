from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'), #
    path('new/<int:group_id>/<str:bm>/', views.post_new, name='post_new'), #
    path('new_one/<int:stend_id>/<int:start_id>/<str:day>/', views.post_new_one, name='post_new_one'), #
    path('new/<int:group_id>/<str:bm>/<int:start_id>/<str:day>/',
         views.post_new_from_table,
         name='post_new_from_table'), #
    path('fib/<int:group_id>/<str:bm>/<int:post_id>/', views.fib_multi_plus, name='fib_multi_plus'), #
    path('day/<str:day>/', views.day, name='day'), #
    path('week/<str:wk>/', views.week, name='week'), #
    path('month/<str:month>/', views.month, name='month'), #
    path('stend/<int:group_id>/', views.stend, name='stend'), #sib, isib, acib
    
    path('404/', views.page_not_found, name='404'), #
    path('500/', views.page_not_found, name='500'), #
    
    path('group/<slug:slug>/', views.group_posts, name='group'), #
    path('group/<slug:slug>/state/<int:state_id>/', #
         views.group_posts_states, name='group_posts_states'),
    path('<str:username>/<int:post_id>/', views.post_view, name='post'), #

    path('<str:username>/<int:post_id>/<int:state_id>/', #
         views.post_view_change, name='post_view_change'),

    path('<str:username>/<int:post_id>/edit/', #
         views.post_edit,
         name='post_edit'),
    path('<str:username>/<int:post_id>/copy/', #
         views.post_copy,
         name='post_copy'),
    path('<str:username>/<int:post_id>/comment/', #
         views.add_comment,
         name='add_comment'),
    
    path('feedbacks/', views.feedbacks, name='feedbacks'), #
    path('feedbacks/add/', views.add_feedback,
         name='add_feedback'), #
    path('feedbacks/delete/<int:feedback_id>/', views.delete_feedback,
         name='delete_feedback'), #
    path('feedbacks/<int:feedback_id>/add/like/<int:user_id>/',
         views.add_like,
         name='add_like'), #
    path('feedbacks/<int:feedback_id>/add/dislike/<int:user_id>/',
         views.add_dislike,
         name='add_dislike'), #
    
    path("<str:username>/<int:post_id>/<int:comment_id>/delete", #
         views.delete_comment,
         name="delete_comment"),
    path('<str:username>/', views.profile, name='profile'), #
    path('<str:username>/<int:post_id>/delete/', #
         views.post_delete, name='post_delete'),
    path('<str:username>/state/<int:state_id>/', #
         views.profile_state,
         name='profile_state'),
    path('requests/help/', views.help, name='help'),
    path('requests/rele_isib/', views.rele_isib, name='rele_isib'),
    path('requests/rele_isib_cold/', views.rele_isib_cold, name='rele_isib_cold'),
    path('requests/rele/<str:IP>/<str:rele_number>/<str:state>/',
         views.rele_on_off,
         name='rele_on_off'),
    path('requests/statistic/', views.statistic, name='statistic'),
]
