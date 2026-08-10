from django.db import models
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

    @property
    def balance(self):
        gave = self.transactions.filter(transaction_type='GAVE').aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0')
        got = self.transactions.filter(transaction_type='GOT').aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0')
        return gave - got


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('GAVE', 'उधारी दी (You Gave)'),
        ('GOT', 'जमा मिला (You Got)'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['customer', '-date']),
            models.Index(fields=['-date']),
            models.Index(fields=['transaction_type']),
        ]

    def __str__(self):
        return f"{self.customer.name} - {self.get_transaction_type_display()} - ₹{self.amount}"


class CashEntry(models.Model):
    ENTRY_TYPES = [
        ('IN', 'कैश इन (पैसे आए)'),
        ('OUT', 'कैश आउट (पैसे गए)'),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    entry_type = models.CharField(max_length=3, choices=ENTRY_TYPES)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Cash Entries"

    def __str__(self):
        return f"{self.get_entry_type_display()} - ₹{self.amount}"