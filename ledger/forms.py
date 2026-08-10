from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
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
        digits = re.sub(r'\D', '', phone)

        if digits.startswith('91') and len(digits) > 10:
            digits = digits[2:]
        elif digits.startswith('0') and len(digits) > 10:
            digits = digits[1:]

        if len(digits) != 10:
            raise ValidationError("कृपया 10 अंकों का सही फोन नंबर डालें।")
        return digits


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type', 'description', 'date']
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
            'date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['date'].initial = timezone.now().strftime('%Y-%m-%dT%H:%M')