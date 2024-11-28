from django.urls import path

from . import views

urlpatterns = [
    path('<int:bord_id>/', views.task_all, name='task_all'),
    path('out/', views.task_out, name='task_out'),
    path('in/', views.task_in, name='task_in'),
    path('<int:task_id>/', views.task, name='task'),

    path('lol/', views.lol, name='lol'),

    path('bord_invite/<int:bord_id>/<int:user_id>/', views.bord_invite, name='bord_invite'),
    path('bord_leave/<int:bord_id>/<int:user_id>/', views.bord_leave, name='bord_leave'),  
    path('task_state_change/<int:bord_id>/<int:task_id>/<int:new_state_id>/', views.task_state_change, name='task_state_change'),
    path('task_slave_change/<int:bord_id>/<int:task_id>/<int:new_slave_id>/', views.task_slave_change, name='task_slave_change'),
    path('task_persent_change/<int:bord_id>/<int:task_id>/<int:persent>/', views.task_persent_change, name='task_persent_change'),

    path('task_all_alter/<int:bord_id>/', views.task_all_alter, name='task_all_alter'),


    path('new/<int:card_id>/', views.task_new, name='task_new'),
    path('card_new/<int:bord_id>/', views.card_new, name='card_new'),
    path('card_rename/<int:bord_id>/<int:card_id>/', views.card_rename, name='card_rename'),

    path('bord_new/', views.bord_new, name='bord_new'),

    path('task_delete/<int:bord_id>/<int:task_id>/', views.task_delete, name='task_delete'),
    path('card_delete/<int:bord_id>/<int:card_id>/', views.card_delete, name='card_delete'),
    path('bord_delete/<int:bord_id>/', views.bord_delete, name='bord_delete'),
    path('bord_rename/<int:bord_id>/', views.bord_rename, name='bord_rename'),

]
