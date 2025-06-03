from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import LocalOrderForm
from lucid_bank.models import LucidBank, Saman

# Create your views here.

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

def new_local_order(request):
    form = LocalOrderForm()
    if request.method == 'POST':
        form = LocalOrderForm(request.POST)
        if form.is_valid():
            local_order_instance = form.save()
            # debit from LucidBank account
            # Get the current balance from LucidBank
            lucid_bank_balance = get_current_balance('lucidity')
            # Get the form data
            date = form.cleaned_data['date']
            transaction ="Local Order",
            debit = local_order_instance.amount
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
            messages.success(request, "Congrats, the local order has been registered!")
            return redirect('local_orders:new_local_order')  # Redirect to the same form or another page
        else:
            form = LocalOrderForm()

    return render(request, 'local_orders/local_order_form.html', {'form': form})