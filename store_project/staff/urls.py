from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff_list, name='staff_list'),
    path('add/', views.add_staff, name='add_staff'),
]
