from django.utils.timezone import now
from decimal import Decimal
from django.db import models

class SaOrder(models.Model):
    date = models.DateTimeField(default=now)

    COMPANY_CHOICES = [
        ('adendorff', 'Adendorff'),
        ('chemvulc', 'Chemvulc'),
        ('academy', 'Academy'),
        ('tools_wholesale', 'Tools Wholesale'),
        ('resolute_supplies', 'Resolute Supplies'),
        ('other', 'Other'),
    ]

    companies = models.JSONField(
        default=list,
        help_text="List of selected company keys (e.g. ['adendorff', 'chemvulc'])"
    )

    # Rand amount for the order
    zar_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
        help_text="The total order cost in ZAR"
    )

    # the rate business used to convert USD to ZAR
    my_zar_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
        help_text="The ZAR rate for USD conversion"
    )

    # the rate the business gave the client
    client_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
        help_text="The conversion rate given to the client"
    )

    usd_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False)
    
    # the usd amount will be calculated using this method
    def get_usd_amount(self):
        return self.zar_amount / self.my_zar_rate
    
    # the markup percentage the business added to the order
    # 32% is the default markup percentage
    markup = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=32.0, 
        blank=True, 
        null=False)

    # order costs in rands
    pick_up_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
        help_text="Cost for picking from companies in ZAR"
    )
    transport_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
        help_text="Cost for transporting to Zim in ZAR"
    )


    transport_cost_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1.0,
        blank=False,
        null=False,
        help_text="The rate used to convert transport cost from USD to ZAR"
    )

    delivery_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
        help_text="Cost for delivery to client in Zim in USD"
    )
   
    # the total cost of the order
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False
    )
    def get_total_cost(self):
        pick_up_cost_to_usd = round(self.pick_up_cost / self.my_zar_rate, 2)
        transport_cost_to_usd = round(self.transport_cost / self.transport_cost_rate, 2)
        return pick_up_cost_to_usd + transport_cost_to_usd + self.delivery_cost
    
    # order revenue
    revenue = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False
    )

    # the total revenue of the order
    def get_revenue(self):
        mark_up = (self.markup / 100) + 1
        # calculate revenue based on client rate
        new_usd_amount = self.zar_amount / self.client_rate
        # calculate revenue based on the new USD amount
        return new_usd_amount * mark_up
    
    # revenue with VAT
    revenue_vat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False
    )
    # the VAT revenue will be calculated using this method
    def get_revenue_vat(self):
        vat = Decimal(0.15 + 1) # 15% VAT
        return self.revenue * vat
    
    # order profit
    profit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False
    )

    internal_bank_deduction = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
    )
    # the internal bank deduction will be calculated using this method
    def get_internal_bank_deduction(self):
        return self.usd_amount + self.total_cost
    
    # the profit will be calculated using this method
    def get_profit(self):
        return self.revenue - self.internal_bank_deduction
    
    order_delivered = models.BooleanField(
        default=False,
        help_text="Has the order been delivered?"
    )
    
    # extra order notes
    notes = models.TextField(
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        # calculate the USD amount
        self.usd_amount = self.get_usd_amount()
        # calculate the total cost
        self.total_cost = self.get_total_cost()
        # calculate the revenue
        self.revenue = self.get_revenue()
        # calculate revenue with VAT
        self.revenue_vat = self.get_revenue_vat()
        # calculate the internal bank deduction
        self.internal_bank_deduction = self.get_internal_bank_deduction()
        # calculate the profit
        self.profit = self.get_profit()
        super(SaOrder, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} - {self.companies} | {self.zar_amount} ZAR"
    class Meta:
        verbose_name = "SA Order"
        verbose_name_plural = "SA Orders"