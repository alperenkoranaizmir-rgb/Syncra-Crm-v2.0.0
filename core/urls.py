from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('samples/', views.sample_list, name='sample_list'),
    path('samples/<int:pk>/', views.sample_detail, name='sample_detail'),
]
