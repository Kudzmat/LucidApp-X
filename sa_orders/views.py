from django.shortcuts import render
from .forms import SaOrderForm

# Create your views here.
def new_order(request):
    form = SaOrderForm()
    if request.method == 'POST':
        form = SaOrderForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect or show success message
    
    context = {
        'form': form,
    }
    return render(request, 'sa_orders/order_form.html', context)


