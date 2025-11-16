from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('samples/', views.sample_list, name='sample_list'),
    path('samples/<int:pk>/', views.sample_detail, name='sample_detail'),
    path('forms/general/', views.forms_general, name='forms_general'),
    path('forms/advanced/', views.forms_advanced, name='forms_advanced'),
    path('forms/validation/', views.forms_validation, name='forms_validation'),
]
