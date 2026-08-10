from django.urls import path
from . import views

urlpatterns = [
    path('', views.daily_ledger, name='daily_ledger'),
    path('add-customer/', views.add_customer, name='add_customer'),
    path('edit-customer/<int:customer_id>/', views.edit_customer, name='edit_customer'),
    path('delete-customer/<int:customer_id>/', views.delete_customer, name='delete_customer'),

    path('entry/<int:customer_id>/', views.add_transaction, name='add_transaction'),
    path('edit-transaction/<int:transaction_id>/', views.edit_transaction, name='edit_transaction'),
    path('delete-transaction/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),

    path('customer/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('customer/<int:customer_id>/print/', views.print_customer, name='print_customer'),

    path('bulk-reminder/', views.bulk_reminder, name='bulk_reminder'),
    path('export-csv/', views.export_csv, name='export_csv'),

    # कैशबुक
    path('cashbook/', views.cashbook, name='cashbook'),
    path('cashbook/add/', views.add_cash_entry, name='add_cash_entry'),
    path('cashbook/delete/<int:entry_id>/', views.delete_cash_entry, name='delete_cash_entry'),
]