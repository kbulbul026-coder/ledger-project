from django import forms
from django.core.exceptions import ValidationError
from .models import Customer, Transaction
import re

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ग्राहक का नाम'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '10 अंकों का फोन नंबर',
                'maxlength': '15'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'पता (वैकल्पिक)'
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        
        # सिर्फ अंक निकालें
        digits = re.sub(r'\D', '', phone)
        
        # +91 या 91 हटाएँ
        if digits.startswith('91') and len(digits) > 10:
            digits = digits[2:]
        elif digits.startswith('0') and len(digits) > 10:
            digits = digits[1:]
            
        if len(digits) != 10:
            raise ValidationError("कृपया 10 अंकों का सही फोन नंबर डालें।")
        
        return digits   # हमेशा 10 डिजिट सेव होगा


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'रकम'
            }),
            'transaction_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'सामान का नाम / नोट'
            }),
        }