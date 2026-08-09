from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.utils import timezone
from django.http import HttpResponse
from decimal import Decimal
import csv

from .models import Customer, Transaction
from .forms import CustomerForm, TransactionForm


@login_required
def daily_ledger(request):
    query = request.GET.get('q', '').strip()
    customers = Customer.objects.all().order_by('name')

    if query:
        customers = customers.filter(
            Q(name__icontains=query) | Q(phone__icontains=query)
        )

    customer_data = []
    total_udhaar = Decimal('0')

    for cust in customers:
        balance = cust.balance
        if balance > 0:
            total_udhaar += balance
        customer_data.append({
            'id': cust.id,
            'name': cust.name,
            'phone': cust.phone,
            'balance': balance,
        })

    today = timezone.now().date()

    today_recovered = Transaction.objects.filter(
        transaction_type='GOT',
        date__date=today
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    today_transactions = Transaction.objects.filter(
        date__date=today
    ).select_related('customer').order_by('-date')

    context = {
        'customers': customer_data,
        'total_udhaar': total_udhaar,
        'today_recovered': today_recovered,
        'today_transactions': today_transactions,
        'query': query,
    }
    return render(request, 'ledger/dashboard.html', context)


@login_required
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('daily_ledger')
    else:
        form = CustomerForm()
    return render(request, 'ledger/add_customer.html', {'form': form})


@login_required
def add_transaction(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.customer = customer
            transaction.save()
            return redirect('customer_detail', customer_id=customer.id)
    else:
        form = TransactionForm()

    return render(request, 'ledger/add_transaction.html', {
        'form': form,
        'customer': customer,
    })


@login_required
def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    transactions = customer.transactions.all()

    return render(request, 'ledger/customer_detail.html', {
        'customer': customer,
        'transactions': transactions,
    })


@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="udhaar_report.csv"'

    writer = csv.writer(response)
    
    # हेडर
    writer.writerow(['नाम', 'फोन', 'पता', 'कुल बकाया (₹)', 'स्थिति'])

    for cust in Customer.objects.all().order_by('name'):
        balance = cust.balance
        status = "उधारी बाकी" if balance > 0 else ("जमा" if balance < 0 else "क्लियर")
        
        writer.writerow([
            cust.name,
            f'="{cust.phone}"',      # Excel में 0 सुरक्षित रहेगा
            cust.address,
            balance,
            status
        ])

    return response




@login_required
def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', customer_id=customer.id)
    else:
        form = CustomerForm(instance=customer)
    
    return render(request, 'ledger/edit_customer.html', {
        'form': form,
        'customer': customer,
    })


@login_required
def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == 'POST':
        customer.delete()
        return redirect('daily_ledger')
    
    return render(request, 'ledger/confirm_delete.html', {
        'object': customer,
        'type': 'customer',
        'name': customer.name,
        'balance': customer.balance,
    })


@login_required
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    customer = transaction.customer
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', customer_id=customer.id)
    else:
        form = TransactionForm(instance=transaction)
    
    return render(request, 'ledger/edit_transaction.html', {
        'form': form,
        'transaction': transaction,
        'customer': customer,
    })


@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    customer_id = transaction.customer.id
    
    if request.method == 'POST':
        transaction.delete()
        return redirect('customer_detail', customer_id=customer_id)
    
    return render(request, 'ledger/confirm_delete.html', {
        'object': transaction,
        'type': 'transaction',
        'name': f"{transaction.get_transaction_type_display()} - ₹{transaction.amount}",
        'customer_name': transaction.customer.name,
    })


@login_required
def print_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    transactions = customer.transactions.all()
    
    return render(request, 'ledger/print_customer.html', {
        'customer': customer,
        'transactions': transactions,
    })

