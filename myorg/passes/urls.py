from django.urls import path

from . import views

urlpatterns = [
    path('', views.all_passes, name='all_passes'),
    path('new/', views.pass_new, name='pass_new'),
    path('copy/<int:pass_id>/', views.pass_copy, name='pass_copy'),
    path('delete/<int:pass_id>/', views.pass_delete, name='pass_delete'),
    path('edit/<int:pass_id>/', views.pass_edit, name='pass_edit'),
    path('filtr/<str:sec_name>/', views.pass_name_filtr, name='pass_name_filtr'),
    path('search/', views.pass_search, name='pass_search'),
] 
