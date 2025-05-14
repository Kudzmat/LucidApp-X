from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import LocalOrderForm

# Create your views here.
def new_local_order(request):
    form = LocalOrderForm()
    if request.method == 'POST':
        form = LocalOrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congrats, the local order has been registered!")
            return redirect('local_orders:new_local_order')  # Redirect to the same form or another page
        else:
            form = LocalOrderForm()

    return render(request, 'local_orders/local_order_form.html', {'form': form})