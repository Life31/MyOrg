from django.urls import path

from . import views

urlpatterns = [
    path('test/', views.show_test, name='show_test'),
    path('test/<int:test_id>/', views.test, name='test'),
    path('result/<int:user_id>/<int:test_id>/', views.show_test_result, name='show_test_result'),
    path('redact_test/<int:test_id>/', views.redact_test, name='redact_test'),
    
] 
