from django.urls import path

from . import views

urlpatterns = [
    path('current/', views.current, name='current'), 
    path('new/unit/', views.config_new_unit, name='config_new_unit'),
    path('units/<int:number>/', views.config_units, name='config_units'),
    path('querys/', views.config_querys, name='config_querys'),
    path('querys/new/', views.config_query_creat, name='config_query_creat'),
    path('changes/<int:query_id>/', views.config_changes, name='config_changes'),
    path('changes/<int:query_id>/confirm/',
         views.config_changes_confirm,
         name='config_changes_confirm'),
    path('new/change/', views.config_new_change, name='config_new_change'),
    path('new/change/<int:conf_id>/',
         views.config_from_conf_to_change,
         name='config_from_conf_to_change'),
    path('new/include/<int:unit_id>/', views.config_new_include, name='config_new_include'),
    #---------------------------------------------------------new
    path('units/all/', views.config_units_all, name='config_units_all'),
    path('new/parametr/<int:unit_id>/', views.config_new_parametr, name='config_new_parametr'),
    path('new/changes/<int:config_id>/', views.config_new_changes, name='config_new_changes'),
    path('new/changes_confirm/<int:changes_id>/', views.config_new_changes_confirm, name='config_new_changes_confirm'),
    path('new/config/', views.config_new_config, name='config_new_config'),
    path('current/conf/', views.config_current_config, name='config_current_config'),
    path('current/re_confirm/<int:confirm_id>/', views.config_re_confirm, name='config_re_confirm'),
    path('current/re_change/<int:change_id>/', views.config_re_change, name='config_re_change'),
    path('current/re_unit/<int:unit_id>/', views.config_re_unit, name='config_re_unit'),
    path('current/changes/<int:number>/', views.config_changes_cur, name='config_changes_cur'),
    path('current/config_sib/', views.config_sib, name='config_sib'),
    
    
    #---------------------------------------------------------new
]   
