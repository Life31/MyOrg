from django.urls import path

from . import views

urlpatterns = [
    path('blocks/print/<str:print>/', views.blocks, name='blocks'),
    path('blocks/new/', views.block_new, name='block_new'),
    path('blocks/creat_doc/', views.print_stor_inj, name='print_stor_inj'),
    #path('blocks/creat_week_doc/<str:day>/', views.print_week, name='print_week'),
    path('blocks/edit/<int:id>/', views.block_edit, name='block_edit'),
    path('blocks/<int:filtr>/', views.blocks_sort, name='blocks_sort'),
    path('blocks/on_where/<int:block_id>/<str:on_where>/',
         views.on_where,
         name='on_where'),
    path('blocks/all/', views.blocks_all, name='blocks_all'),
    path('blocks/week/<str:day>/print/<str:Print>/', views.blocks_week, name='blocks_week'),
    path('blocks/event_new/<int:block_id>/', views.pro_event_new, name='pro_event_new'),
    path('blocks/event_all/<int:block_id>/', views.pro_events_all, name='pro_events_all'),

    
    
]
