from django.db import models
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)  # unique = index पहले से है
    address = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),  # नाम से सर्च के लिए
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

    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE, 
        related_name='transactions',
        db_index=True  # ForeignKey पर इंडेक्स (डिफ़ॉल्ट में भी होता है)
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date']
        indexes = [
            # सबसे महत्वपूर्ण: ग्राहक + तारीख
            models.Index(fields=['customer', '-date']),
            
            # सिर्फ तारीख पर फिल्टर के लिए
            models.Index(fields=['-date']),
            
            # प्रकार के हिसाब से
            models.Index(fields=['transaction_type']),
        ]

    def __str__(self):
        return f"{self.customer.name} - {self.get_transaction_type_display()} - ₹{self.amount}"