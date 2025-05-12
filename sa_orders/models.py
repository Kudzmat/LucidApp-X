from django.db import models

# Create your models here.

class SaOrder(models.Model):
    date = models.DateField(blank=False, null=False)

    # options for the company field
    COMPANY_CHOICES = [
        ('adendorff', 'Adendorff'),
        ('chemvulc', 'Chemvulc'),
        ('academy', 'Academy'),
        ('tools_wholesale', 'Tools Wholesale'),
        ('resolute_supplies', 'Resolute Supplies'),
        ('other', 'Other'),
    ]


    company = models.CharField(
        max_length=50,
        choices=COMPANY_CHOICES,
        default='n/a'
    )
    # if 'other' is selected, this field should be filled
    # with the name of the other company
    other_company = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Only fill this if 'Other' is selected"
    )

    # will display the company name in the admin panel
    def get_company_display_name(self):
        if self.company == 'other' and self.other_company:
            return self.other_company
        return self.get_company_display()

    # Rand amount for the order
    zar_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False
    )

    # the rate business used to convert USD to ZAR
    my_zar_rate = models.FloatField(
        blank=False,
        null=False,
        help_text="The ZAR rate for the order"
    )

    # the rate the business gave the client
    client_rate = models.FloatField(
        blank=False,
        null=False,
        help_text="The client rate for the order"
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
    markup = models.FloatField(default=32.0, blank=True, null=False)

    # order costs
    pick_up_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False
    )
    transport_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False
    )
    delivery_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False
    )

    internal_bank_deduction = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False
    )
    # the internal bank deduction will be calculated using this method
    def get_internal_bank_deduction(self):
        return self.zar_amount / self.my_zar_rate
   

    # the total cost of the order
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False
    )
    def get_total_cost(self):
        return self.pick_up_cost + self.transport_cost + self.delivery_cost
    
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
        return self.usd_amount * mark_up
    
    # revenue with VAT
    revenue_vat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False
    )
    # the VAT revenue will be calculated using this method
    def get_revenue_vat(self):
        return self.revenue * 1.15
    
    # order profit
    profit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False
    )
    
    def get_profit(self):
        costs = self.total_cost + self.internal_bank_deduction
        return self.revenue - costs
    
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
        # calculate the internal bank deduction
        self.internal_bank_deduction = self.get_internal_bank_deduction()
        # calculate the revenue
        self.revenue = self.get_revenue()
        # calculate revenue with VAT
        self.revenue_vat = self.get_revenue_vat()
        # calculate the profit
        self.profit = self.get_profit()
        super(SaOrder, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} - {self.get_company_display_name()} - {self.zar_amount} ZAR"
    class Meta:
        verbose_name = "SA Order"
        verbose_name_plural = "SA Orders"
