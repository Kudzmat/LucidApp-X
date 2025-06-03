from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Saman, LucidBank, AccountBalance
from .forms import *


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

def get_owed_balance():
    last_entry = AccountBalance.objects.order_by('-date').first()

    if last_entry:
        current_balance = last_entry.balance
    else:
        current_balance = 0  # Default value if no entries exist

    return current_balance


# Create your views here.
def withdrawal(request):
    form = WithdrawalForm()
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            
            # if user is withdrawing from lucid bank
            if form.cleaned_data['withdraw_from'] == 'lucidity':
                # get current balance from database
                # Get the most recent entry based on the 'date' field
                current_balance = get_current_balance('lucidity')

                # get the data from the form
                date = form.cleaned_data['date']
                bank = form.cleaned_data['withdraw_from']
                transaction = form.cleaned_data['transaction']
                debit= form.cleaned_data['amount']
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
                
            elif form.cleaned_data['withdraw_from'] == 'saman':
                # get current balance from database
                # Get the most recent entry based on the 'date' field
                current_balance = get_current_balance('saman')
                print(current_balance)
                

                # get the data from the form
                date = form.cleaned_data['date']
                bank = form.cleaned_data['withdraw_from']
                transaction = form.cleaned_data['transaction']
                debit = form.cleaned_data['amount']
                credit = 0
                notes = form.cleaned_data['notes']

                # calculate the balance
                balance = current_balance - debit

                # create a new Saman instance
                saman = Saman.objects.create(
                    date=date,
                    transaction=transaction,
                    debit=debit,
                    credit=credit,
                    balance=balance,
                    notes=notes
                )
                saman.save()
                messages.success(request, f"Congrats, the ${debit} withdrawal from {bank} bank has been registered!")
                return redirect('lucid_bank:bank_withdrawal')
            else:
                form = WithdrawalForm()
    return render(request, 'lucid_bank/withdrawal_form.html', {'form': form})

def make_payment(request):
    form = PaymentForm()
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            
            # if user is paying to lucidity
            if form.cleaned_data['pay_to'] == 'lucidity':
                # get current balance from database
                # Get the most recent entry based on the 'date' field
                current_balance = get_current_balance('lucidity')

                # get the data from the form
                date = form.cleaned_data['date']
                bank = form.cleaned_data['pay_to']
                transaction = form.cleaned_data['transaction']
                amount = form.cleaned_data['amount']
                notes = form.cleaned_data['notes']

                # calculate the balance
                balance = current_balance + amount
                
                # create a new LucidBank instance
                lucid_bank = LucidBank.objects.create(
                    date=date,
                    transaction=transaction,
                    debit=0,
                    credit=amount,
                    balance=balance,
                    notes=notes
                )
                lucid_bank.save()
                
                messages.success(request, f"Congrats, the ${amount} payment to {bank} bank has been registered!")
                return redirect('lucid_bank:make_payment')  # Redirect to the same form or another page
            
            # if user is paying to Saman
            elif form.cleaned_data['pay_to'] == 'saman':
                # get current balance from database
                # Get the most recent entry based on the 'date' field
                current_balance = get_current_balance('saman')
                print(current_balance)

                # get the data from the form
                date = form.cleaned_data['date']
                bank = form.cleaned_data['pay_to']
                transaction = form.cleaned_data['transaction']
                amount = form.cleaned_data['amount']
                notes = form.cleaned_data['notes']

                # calculate the balance
                balance = current_balance + amount
                print(balance)

                # create a new Saman instance
                saman = Saman.objects.create(
                    date=date,
                    transaction=transaction,
                    debit=0,
                    credit=amount,
                    balance=balance,
                    notes=notes
                )
                saman.save()

                messages.success(request, f"Congrats, the ${amount} payment to {bank} bank has been registered!")
                return redirect('lucid_bank:make_payment')
            else:
                form = PaymentForm()
    return render(request, 'lucid_bank/make_payment.html', {'form': form})

def make_transfer(request):
    form = TransferForm()
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            
            # if user is transferring from lucid bank
            if form.cleaned_data['pay_from'] == 'lucidity' and form.cleaned_data['pay_to'] == 'saman':
                # get current balance from database
                # Get lucidity bank balance
                current_balance_lucid = get_current_balance('lucidity')
                
                # get Saman bank balance
                current_balance_saman = get_current_balance('saman')

                # get the data from the form
                date = form.cleaned_data['date']
                bank = form.cleaned_data['pay_from']
                transaction = form.cleaned_data['transaction']
                debit = form.cleaned_data['amount']
                credit = 0
                notes = form.cleaned_data['notes']

                # debit lucidity bank
                # calculate the balance
                balance_lucid = current_balance_lucid - debit 

                # create a new LucidBank instance
                lucid_bank = LucidBank.objects.create(
                    date=date,
                    transaction=transaction,
                    debit=debit,
                    credit=credit,
                    balance=balance_lucid,
                    notes=notes
                )
                lucid_bank.save()

                # credit Saman bank
                # calculate the balance
                balance_saman = current_balance_saman + debit

                # create a new Saman instance
                saman = Saman.objects.create(
                    date=date,
                    transaction=transaction,
                    debit=0,
                    credit=debit,
                    balance=balance_saman,
                    notes=notes
                )
                saman.save()

                messages.success(request, f"Congrats, the ${debit} transfer from {bank} bank has been registered!")
                return redirect('lucid_bank:make_transfer')  # Redirect to the same form or another page
            
            elif form.cleaned_data['pay_from'] == 'saman' and form.cleaned_data['pay_to'] == 'lucidity':
                # get current balance from database
                # Get lucidity bank balance
                current_balance_lucid = get_current_balance('lucidity')
                
                # get Saman bank balance
                current_balance_saman = get_current_balance('saman')

                # get the data from the form
                date = form.cleaned_data['date']
                bank = form.cleaned_data['pay_from']
                transaction = form.cleaned_data['transaction']
                debit = form.cleaned_data['amount']
                credit = 0
                notes = form.cleaned_data['notes']

                # debit Saman bank
                # calculate the balance
                balance_saman = current_balance_saman - debit 

                                # create a new Saman instance
                saman = Saman.objects.create(
                    date=date,
                    transaction=transaction,
                    debit=debit,
                    credit=credit,
                    balance=balance_saman,
                    notes=notes
                )
                saman.save()

                # credit lucidity bank
                # calculate the balance
                balance_lucid = current_balance_lucid + debit

                # create a new LucidBank instance
                lucid_bank = LucidBank.objects.create(
                    date=date,
                    transaction=transaction,
                    debit=0,
                    credit=debit,
                    balance=balance_lucid,
                    notes=notes
                )
                lucid_bank.save()

                messages.success(request, f"Congrats, the ${debit} transfer from {bank} bank has been registered!")
                return redirect('lucid_bank:make_transfer')
            else:
                form = TransferForm()
    return render(request, 'lucid_bank/transfer_form.html', {'form': form})


def view_statement(request):
    bank = request.GET.get('bank', 'lucid')  # Default to 'lucid' if no bank is selected
    if bank == 'lucid':
        transactions = LucidBank.objects.order_by('-date')  # Order by most recent
        bank_name = "Lucid Bank"
    elif bank == 'saman':
        transactions = Saman.objects.order_by('-date')  # Order by most recent
        bank_name = "Saman Bank"
    else:
        transactions = []
        bank_name = "Unknown Bank"

    context = {
        'transactions': transactions,
        'bank_name': bank_name,
    }
    return render(request, 'lucid_bank/view_statement.html', context)

def balance_payment(request):
    # show user current balance owed by client
    current_owed_balance = get_owed_balance()
    form = BalancePaymentForm()
    if request.method == 'POST':
        form = BalancePaymentForm(request.POST)
        if form.is_valid():
            print(f"paying to {form.cleaned_data['pay_to']}")
            # if user is paying to lucid bank
            if form.cleaned_data['pay_to'] == 'lucidity':
                # get current balance from database
                # Get the most recent entry based on the 'date' field
                current_balance = get_current_balance('lucidity')

                # get the data from the form
                date = form.cleaned_data['date']
                bank = form.cleaned_data['pay_to']
                transaction = form.cleaned_data['transaction']
                amount = form.cleaned_data['amount']
                notes = form.cleaned_data['notes']

                # calculate the balance
                balance = current_balance + amount
                
                # create a new LucidBank instance
                lucid_bank = LucidBank.objects.create(
                    date=date,
                    transaction=transaction,
                    debit=0,
                    credit=amount,
                    balance=balance,
                    notes=notes
                )
                lucid_bank.save()

                # subtract the amount from the balance owed by client
                # get latest account balance owed
                new_balance = current_owed_balance - amount
                # create new AccountBalance instance
                owed_balance_instance = AccountBalance.objects.create(
                    date=date,
                    transaction=transaction,
                    debit=amount,
                    credit=0,
                    balance=new_balance,
                )
                owed_balance_instance.save()
                
                messages.success(request, f"Congrats, the ${amount} payment to {bank} bank has been registered!")
                return redirect('lucid_bank:balance_payment')
            
            # if user is paying to Saman
            elif form.cleaned_data['pay_to'] == 'saman':
                # get current balance from database
                # Get the most recent entry based on the 'date' field
                current_balance = get_current_balance('saman')

                # get the data from the form
                date = form.cleaned_data['date']
                bank = form.cleaned_data['pay_to']
                transaction = form.cleaned_data['transaction']
                amount = form.cleaned_data['amount']
                notes = form.cleaned_data['notes']

                # calculate the balance
                balance = current_balance + amount

                # create a new Saman instance
                saman = Saman.objects.create(
                    date=date,
                    transaction=transaction,
                    debit=0,
                    credit=amount,
                    balance=balance,
                    notes=notes
                )
                saman.save()

                # subtract the amount from the balance owed by client
                # get latest account balance owed
                new_balance = current_owed_balance - amount
                # create new AccountBalance instance
                owed_balance_instance = AccountBalance.objects.create(
                    date=date,
                    transaction=transaction,
                    debit=amount,
                    credit=0,
                    balance=new_balance,
                )
                owed_balance_instance.save()

                messages.success(request, f"Congrats, the amount has been deducted from owed balances!")
                return redirect('lucid_bank:balance_payment')
            else:
                form = BalancePaymentForm()

    context = {'form': form, 'current_owed_balance': current_owed_balance}

    return render(request, 'lucid_bank/balance_payment.html',context=context)