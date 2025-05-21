from django.shortcuts import render, redirect
from django.contrib import messages
from local_orders.models import LocalOrder
from sa_orders.models import SaOrder
from lucid_bank.models import AccountBalance

def view_orders(request):
    # Fetch all orders from LocalOrder and SaOrder
    local_orders = LocalOrder.objects.all()
    sa_orders = SaOrder.objects.all()

    if request.method == 'POST':
        # Handle toggling of the order_delivered option
        order_type = request.POST.get('order_type')  # 'local' or 'sa'
        order_id = request.POST.get('order_id')

        if order_type == 'local':
            order = LocalOrder.objects.get(id=order_id)
        elif order_type == 'sa':
            order = SaOrder.objects.get(id=order_id)
        else:
            order = None

        if order:
            # Toggle the order_delivered status
            order.order_delivered = not order.order_delivered
            order.save()

            # If the order is marked as delivered, create a Balance instance
            if order.order_delivered:
                new_balance = AccountBalance.objects.create(
                    total_amount=order.revenue_vat,  # Assuming revenue_vat is the total amount owed
                    actual_amount=0  # Use the method to calculate the actual amount
                )
                new_balance.save()
                messages.success(request, f"Order {order.id} marked as delivered and Balance created.")
            else:
                messages.info(request, f"Order {order.id} marked as not delivered.")

        return redirect('performance:view_orders')

    context = {
        'local_orders': local_orders,
        'sa_orders': sa_orders,
    }
    return render(request, 'performance/orders.html', context)