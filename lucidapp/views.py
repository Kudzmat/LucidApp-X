from django.shortcuts import render
from django.utils.timezone import now
from django.db.models import Sum
from local_orders.models import LocalOrder
from sa_orders.models import SaOrder
from lucid_bank.models import LucidBank, Saman

# Dashboard view
def home(request):
    # Get the current month
    current_month = now().strftime('%B %Y')

    # Total orders
    total_sa_orders = SaOrder.objects.count()
    total_local_orders = LocalOrder.objects.count()
    total_orders = total_sa_orders + total_local_orders

    # Total value of orders
    total_sa_value = SaOrder.objects.aggregate(total_value=Sum('revenue'))['total_value'] or 0
    total_local_value = LocalOrder.objects.aggregate(total_value=Sum('revenue'))['total_value'] or 0
    total_order_value = round(total_sa_value + total_local_value, 2)

    # Cash in banks
    lucid_bank_balance = LucidBank.objects.order_by('-date').first().balance if LucidBank.objects.exists() else 0
    saman_balance = Saman.objects.order_by('-date').first().balance if Saman.objects.exists() else 0

    # Orders not delivered
    sa_orders_not_delivered = SaOrder.objects.filter(order_delivered=False).count()
    local_orders_not_delivered = LocalOrder.objects.filter(order_delivered=False).count()
    total_orders_not_delivered = sa_orders_not_delivered + local_orders_not_delivered

    context = {
        'current_month': current_month,
        'total_orders': total_orders,
        'total_sa_orders': round(total_sa_value, 2),
        'total_local_orders': round(total_local_value, 2),
        'total_order_value': total_order_value,
        'lucid_bank_balance': lucid_bank_balance,
        'saman_balance': saman_balance,
        'total_orders_not_delivered': total_orders_not_delivered,
    }

    return render(request, 'index.html', context)