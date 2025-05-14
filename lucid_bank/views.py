from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Saman, LucidBank
from .forms import *

# Create your views here.
def withdrawal(request):
    form = WithdrawalForm()
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            
            # if user is withdrawing from lucid bank
            if form.cleaned_data['bank'] == 'lucidity':
                # get current balance from database
                # Get the most recent entry based on the 'date' field
                last_entry = LucidBank.objects.order_by('-date').first()
                if last_entry:
                    current_balance = last_entry.balance
                else:
                    current_balance = 0  # Default value if no entries exist

                # get the data from the form
                date = form.cleaned_data['date']
                bank = form.cleaned_data['bank']
                transaction = form.cleaned_data['transaction']
                debit = form.cleaned_data['debit']
                credit = 0
                notes = form.cleaned_data['notes']

                # calculate the balance
                balance = current_balance - debit

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
                messages.success(request, f"Congrats, the ${debit} withdrawal from {bank} bank has been registered!")
                return redirect('lucid_bank:bank_withdrawal')  # Redirect to the same form or another page
        else:
            form = WithdrawalForm()
    return render(request, 'lucid_bank/withdrawal_form.html', {'form': form})