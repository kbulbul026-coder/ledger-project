from django import forms
from .models import Customer, Transaction

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
                'placeholder': 'फोन नंबर'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'पता (वैकल्पिक)'
            }),
        }


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