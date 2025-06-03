from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from local_orders.models import LocalOrder
from sa_orders.models import SaOrder
from lucid_bank.models import AccountBalance
from datetime import date, datetime

def get_owed_balance():
    last_entry = AccountBalance.objects.order_by('-date').first()

    if last_entry:
        current_balance = last_entry.balance
    else:
        current_balance = 0  # Default value if no entries exist

    return current_balance

def view_orders(request):
    # Get the selected month from the query parameters
    selected_month = request.GET.get('month', datetime.now().strftime('%Y-%m'))  # Default to the current month

    # Parse the selected month into year and month
    try:
        # Split the selected_month string (e.g., "2025-05") into year and month as integers.
        # map(int, ...) converts the split strings into integers.
        year, month = map(int, selected_month.split('-'))
    except ValueError:
        # If the selected_month is invalid (e.g., not in "YYYY-MM" format),
        # fall back to the current year and month using datetime.now().
        year, month = datetime.now().year, datetime.now().month

    # Filter orders by the selected month
    local_orders = LocalOrder.objects.filter(date__year=year, date__month=month)
    sa_orders = SaOrder.objects.filter(date__year=year, date__month=month)

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

            if order.order_delivered:
            # first get latest balance
                owed_balance = get_owed_balance()
                new_balance = owed_balance + order.revenue_vat
                
                # If the order is marked as delivered, create a Balance instance
                new_balance = AccountBalance.objects.create(
                    date=order.date,
                    transaction=f"Payment for {'local' if order_type == 'local' else 'SA'} order {order.id} | ${order.revenue_vat}",
                    balance=new_balance,
                    debit=0,  # Assuming no debit for this balance
                    credit=order.revenue_vat   # Assuming no credit for this balance
                )
                new_balance.save()
                messages.success(request, f"Order {order.id} marked as delivered and Balance created.")
            else:
                messages.info(request, f"Order {order.id} marked as not delivered.")

        return redirect('performance:view_orders')

    context = {
        'local_orders': local_orders,
        'sa_orders': sa_orders,
        'selected_month': selected_month,
    }
    return render(request, 'performance/orders.html', context)

def view_monthly_performance(request):
    # Get the selected month from the query parameters
    selected_month = request.GET.get('month', datetime.now().strftime('%Y-%m'))  # Default to the current month

    # Parse the selected month into year and month
    try:
        year, month = map(int, selected_month.split('-'))
    except ValueError:
        year, month = datetime.now().year, datetime.now().month

    # Aggregate daily revenue for the selected month
    local_orders = LocalOrder.objects.filter(date__year=year, date__month=month).values('date').annotate(
        daily_revenue=Sum('amount')
    )
    sa_orders = SaOrder.objects.filter(date__year=year, date__month=month).values('date').annotate(
        daily_revenue=Sum('revenue')
    )

    # Get combined order data
    order_data = get_order_data(local_orders, sa_orders)

    # Prepare data for the chart
    labels = list(order_data.keys())  # Days of the month
    chart_data = list(order_data.values())  # Revenue for each day

    context = {
        'selected_month': selected_month,
        'labels': labels,
        'chart_data': chart_data,
    }
    return render(request, 'performance/month_charts.html', context)

# function to combine local and SA orders into a single dictionary
def get_order_data(local_orders, sa_orders):
    """
    Combine local and SA orders into a single dictionary with day as the key and amount as the value.
    """
    day_and_amount = {}

    # Process local orders
    for order in local_orders:
        date = order['date']  # Assuming 'date' is a datetime object
        day = date.day  # Extract the day of the month
        amount = float(round(order['daily_revenue'], 2))
        day_and_amount[day] = day_and_amount.get(day, 0) + amount

    # Process SA orders
    for order in sa_orders:
        date = order['date']
        day = date.day  # Extract the day of the month
        amount = float(round(order['daily_revenue'], 2))
        day_and_amount[day] = day_and_amount.get(day, 0) + amount

    return day_and_amount

def view_yearly_performance(request):
    # Define a dictionary to map month numbers to month names
    months = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April', 
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }
    # Get the selected year from the query parameters
    selected_year = request.GET.get('year', datetime.now().year)  # Default to the current year

    # Parse the selected year
    try:
        year = int(selected_year)
    except ValueError:
        year = datetime.now().year

    # Aggregate monthly revenue for the selected year
    local_orders = LocalOrder.objects.filter(date__year=year).values('date__month').annotate(
        monthly_revenue=Sum('revenue')
    )
    sa_orders = SaOrder.objects.filter(date__year=year).values('date__month').annotate(
        monthly_revenue=Sum('revenue')
    )
    year_data = get_year_data(local_orders, sa_orders)

    # Prepare data for the chart
    labels = [months[i] for i in range(1, 13)]  # Month names
    chart_data = [year_data.get(i, 0) for i in range(1, 13)]  # Revenue for each month, defaulting to 0 if no data

    context = {
        'selected_year': selected_year,
        'labels': labels,
        'chart_data': chart_data,
    }
    return render(request, 'performance/yearly_performance.html', context)

def get_year_data(local_orders, sa_orders):
    """
    Combine local and SA orders into a single dictionary with month as the key and amount as the value.
    """
    month_and_amount = {}

    # Process local orders
    for order in local_orders:
        month = order['date__month']  # Assuming 'date__month' is an integer representing the month
        amount = float(round(order['monthly_revenue'], 2))
        month_and_amount[month] = month_and_amount.get(month, 0) + amount

    # Process SA orders
    for order in sa_orders:
        month = order['date__month']
        amount = float(round(order['monthly_revenue'], 2))
        month_and_amount[month] = month_and_amount.get(month, 0) + amount

    return month_and_amount