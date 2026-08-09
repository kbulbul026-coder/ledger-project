from django.urls import path
from . import views

urlpatterns = [
    path('', views.daily_ledger, name='daily_ledger'),
    path('add-customer/', views.add_customer, name='add_customer'),
    path('entry/<int:customer_id>/', views.add_transaction, name='add_transaction'),
    path('customer/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('export-csv/', views.export_csv, name='export_csv'),
]
