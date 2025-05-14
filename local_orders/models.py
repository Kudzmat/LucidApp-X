from decimal import Decimal
from django.db import models

# Create your models here.
class LocalOrder(models.Model):
    date = models.DateField(blank=False, null=False)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
        help_text="The cost of the order in USD"
    )

    # markup default is 17%
    markup = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=17.5, 
        blank=True, 
        null=False)
    
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
        return self.amount * mark_up
    
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

    # the profit will be calculated using this method
    def get_profit(self):
        return self.revenue - self.amount
    
    # extra order notes
    notes = models.TextField(
        blank=True,
        null=True
    )
    
    def save(self, *args, **kwargs):
        # calculate the revenue
        self.revenue = self.get_revenue()
        # calculate the revenue with VAT
        self.revenue_vat = self.get_revenue_vat()
        # calculate the profit
        self.profit = self.get_profit()
        
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Local Order {self.date} - {self.amount} USD"
    

