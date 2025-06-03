from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SaOrderForm
from .models import *
from lucid_bank.models import LucidBank, Saman

def get_current_balance(bank):
    if bank == 'lucidity':
        last_entry = LucidBank.objects.order_by('-date').first()
    elif bank == 'saman':
        last_entry = Saman.objects.order_by('-date').first()
    else:
        last_entry = 0

    if last_entry:
        current_balance = last_entry.balance
    else:
        current_balance = 0  # Default value if no entries exist

    return current_balance


def new_sa_order(request):
    if request.method == 'POST':
        form = SaOrderForm(request.POST)
        if form.is_valid():
            sa_order_instance = form.save()

            # debit from LucidBank account
            # Get the current balance from LucidBank
            lucid_bank_balance = get_current_balance('lucidity')
            # Get the form data
            date = form.cleaned_data['date']
            transaction = f"SA Order - {form.cleaned_data['companies']}"
            debit = sa_order_instance.internal_bank_deduction
            credit = 0
            balance = lucid_bank_balance - debit
            notes = form.cleaned_data['notes']
            
            # create a new LucidBank instance
            lucid_bank = LucidBank.objects.create(
                date=date,
                transaction=transaction,
                debit=debit,
                credit=credit,
                balance=balance,
                notes=notes
            )
            lucid_bank.save()
            messages.success(request, "Congrats, the SA order has been registered!")
            return redirect('sa_orders:new_sa')  # Redirect to the same form or another page
    else:
        form = SaOrderForm()

    return render(request, 'sa_orders/order_form.html', {'form': form})


