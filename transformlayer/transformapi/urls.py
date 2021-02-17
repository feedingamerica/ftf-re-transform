from django.urls import path

from . import views

urlpatterns = [
    path('api/', views.test_endpoint_1, name='api'),
    path('about/', views.test_endpoint_2, name='about'),
    path('data/', views.test_data_service, name='data')
]