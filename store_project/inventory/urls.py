from django.urls import path
from . import views

urlpatterns = [
    # Products
    path('', views.product_list, name='product_list'),
    path('add/', views.add_product, name='add_product'),
    path('update/<int:id>/', views.update_product, name='update_product'),
    path('delete/<int:id>/', views.delete_product, name='delete_product'),

    # Suppliers
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.add_supplier, name='add_supplier'),
    path('suppliers/update/<int:id>/', views.update_supplier, name='update_supplier'),
    path('suppliers/delete/<int:id>/', views.delete_supplier, name='delete_supplier'),

    #stock alert
    path('send-alert/', views.send_low_stock_alert, name='send_low_stock_alert'),
]