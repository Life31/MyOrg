from django.urls import path

from . import views

urlpatterns = [
    path('storage/', views.storage, name='storage'),
    path('unit/new/', views.unit_new, name='unit_new'),
    path('unit/<int:unit_id>/edit/', views.unit_edit, name='unit_edit'),
    path('unit/<int:unit_id>/delete/', views.unit_delete, name='unit_delete'),
    path('unit/<int:id>/', views.unit_ths, name='unit_ths'),
    path('th/new/', views.th_new, name='th_new'),
    path('event/new/<int:unit_id>/', views.event_new, name='event_new'),
    path('event/edit/<int:event_id>/<int:unit_id>/', views.event_edit, name='event_edit'),
    path('th/<int:th_id>/edit/', views.th_edit, name='th_edit'),
    path('th/<int:th_id>/delete/', views.th_delete, name='th_delete'),
    path('main/', views.main, name='main'),
    path('main/likes/', views.main_likes, name='main_likes'),
    
    path('main/by_ctgry/<int:ctgry_id>/', views.units_by_ctgry, name='units_by_ctgry'),
    path('main/by_creator/<int:creator_id>/', views.units_by_creator, name='units_by_creator'),
    path('main/by_place/<int:place_id>/', views.units_by_place, name='units_by_place'),
    path('th_all/', views.th_all, name='th_all'),
    path('th_all/tag/<int:tag_id>/', views.th_all_tag, name='th_all_tag'),
    path('th_all/year/<str:year>/', views.th_all_year, name='th_all_year'),
    path('th_all/type/<str:type_th>/', views.th_all_type, name='th_all_type'),
    path('place_new/', views.place_new, name='place_new'),
    path('creator_new/', views.creator_new, name='creator_new'),
    path('ctgry_new/', views.ctgry_new, name='ctgry_new'),
    path('si_new/', views.si_new, name='si_new'),
    path('stend_new/', views.stend_new, name='stend_new'),
    path('tag_new/', views.tag_new, name='tag_new'),
    path('tag/add/<int:th_id>/', views.tag_add, name='tag_add'),
    path('storage_where/<str:place>/', views.storage_where, name='storage_where'),
    path('unit/search/', views.units_search, name='units_search'),
    path('unit/<int:unit_id>/event/delete/<int:event_id>/', views.event_delete, name='event_delete'),
    path('unit/<int:unit_id>/event/copy/<int:event_id>/', views.event_copy, name='event_copy'),
    path('main/unit_like/<int:unit_id>/', views.unit_like, name='unit_like'),

]
