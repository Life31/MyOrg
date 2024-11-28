from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('users/', views.users, name='users'),
    path('users_access/<str:app>/', views.users_access, name='users_access'),
    path('users_info_change/<int:user_id>/', views.users_info_change, name='users_info_change'),
    path('user_search/', views.user_search, name='user_search'),
    path('users_in_otd/<int:number>/', views.users_in_otd, name='users_in_otd'),
    path('log/', views.log_all, name='log_all'),
    path('vacations/all/<int:year>/<int:otd>/', views.vacations, name='vacations'),
    path('vacations/new/<int:year>/<int:otd>/', views.vacation_new, name='vacation_new'),
    path('vacations/all/', views.vacations_start, name='vacations_start'),
    #path('vacations/all/print/<int:year>/<int:otd>/', views.vacations_print, name='vacations_print'),

    path('vacations/vacation_edit/<int:year>/<int:otd>/<int:vac_id>/', views.vacation_edit, name='vacation_edit'),
    path('vacations/vacation_delete/<int:otd>/<int:year>/<int:vac_id>/', views.vacation_delete, name='vacation_delete'),
    path('vacations/all/vac_by_us/<int:year>/<int:otd>/', views.vacations_by_user, name='vacations_by_user'),
    path('vacations/vacation_confirm/<int:year>/<int:otd>/<int:vac_id>/', views.vacation_confirm, name='vacation_confirm'),
    path('vacations/vacation_confirm/<int:year>/<int:otd>/<str:user>/<str:day>/', views.vacation_confirm_from_day, name='vacation_confirm_from_day'),

    path('vacations/del_vac_by_drop/<int:otd>/<str:user_name>/<str:day>/', views.del_vac_by_drop, name='del_vac_by_drop'),

    path('users/<int:user_id>/', views.user_space, name='user_space'),
    path('users/widget_add/<int:user_id>/<str:widget_name>/', views.user_widget_add, name='user_widget_add'),
    path('users/widget_delete/<int:user_id>/<str:widget_name>/', views.user_widget_delete, name='user_widget_delete'),
    path('users/widget_close/<int:user_id>/<str:widget_name>/<int:widget_id>/', views.user_widget_close, name='user_widget_close'),
    path('users/widget_close_all/<int:user_id>/<str:state>/', views.user_widget_close_all, name='user_widget_close_all'),

    path('users/messages/<int:user_one_id>/<int:user_two_id>/', views.messages, name='messages'),
    path('note_delete/<int:note_id>/', views.note_delete, name='note_delete'),

    path('vacations/vac_2/<int:year>/<int:otd>/', views.vac_2, name='vac_2'),
    path('vacations/add_new_vac/<int:otd>/<int:day_s>/<int:month_s>/<int:year_s>/<int:long>/<int:day_e>/<int:month_e>/<int:user_id>/', views.add_new_vac, name='add_new_vac'),
    path('vacations/vac_edit/<int:otd>/<int:day_s>/<int:month_s>/<int:year_s>/<int:long>/<int:day_e>/<int:month_e>/<int:user_id>/<int:vac_id>/', views.vac_edit, name='vac_edit'),

    path('backup_base/', views.backup_base, name='backup_base'),
    
]
