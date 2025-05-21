from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SaOrderForm
from .models import *

def new_sa_order(request):
    if request.method == 'POST':
        form = SaOrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congrats, the SA order has been registered!")
            return redirect('sa_orders:new_sa')  # Redirect to the same form or another page
    else:
        form = SaOrderForm()

    return render(request, 'sa_orders/order_form.html', {'form': form})


