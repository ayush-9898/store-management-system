from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff_list, name='staff_list'),
    path('add/', views.add_staff, name='add_staff'),
    path('update/<int:id>/', views.update_staff, name='update_staff'),
    path('delete/<int:id>/', views.delete_staff, name='delete_staff'),
]
