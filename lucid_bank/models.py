from decimal import Decimal
from django.utils.timezone import now
from django.db import models


# Create your models here.
class Saman(models.Model):
    date = models.DateTimeField(default=now)
    transaction = models.CharField(max_length=255, blank=False, null=False)
    debit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False
    )
    credit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=False,
        default=0,
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=False,
        default=0,
    )
    notes = models.TextField(
        blank=True,
        null=True,
    )

    def calculate_balance(self, current_balance, debit, credit):
        if debit > 0:
            return current_balance - debit
        elif credit > 0:
            return current_balance + credit
        else:
            return current_balance
    
    def __str__(self):
        if self.debit > 0:
            return f"{self.date} - Debit: {self.debit} | {self.transaction} | Balance: {self.balance}"
        elif self.credit > 0:
            return f"{self.date} - Credit: {self.credit} | {self.transaction} | Balance: {self.balance}"
        else:
            return "No transaction"
  
class LucidBank(models.Model):
    date = models.DateTimeField(default=now)
    transaction = models.CharField(max_length=255, blank=False, null=False)
    debit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=False,
        default=0,
    )
    credit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=False,
        default=0,
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False
    )
    notes = models.TextField(
        blank=True,
        null=True
    )

    def calculate_balance(self, current_balance, debit, credit):
        if debit > 0:
            return current_balance - debit
        elif credit > 0:
            return current_balance + credit
        else:
            return current_balance

    def __str__(self):
        if self.debit > 0:
            return f"{self.date} - Debit: {self.debit} | {self.transaction} | Balance: {self.balance}"
        elif self.credit > 0:
            return f"{self.date} - Credit: {self.credit} | {self.transaction} | Balance: {self.balance}"
        else:
            return "No transaction"
        

class AccountBalance(models.Model):
    """
    A model to store how much money is owed from suppliers.
    """
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
        help_text="The total amount owed to suppliers"
    )

    actual_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
        help_text="The actual amount owed to suppliers"
    )

    # The amount Lucidity will take is calculated using this method
    def get_actual_amount(self):
        vat = Decimal(1.15)
        less_vat = self.total_amount / vat
        # calculate amount with 3% bank withdrawal charge
        bank_charge = Decimal(1.03)
        actual_amount = Decimal(less_vat / bank_charge)
        return actual_amount
    
    def save(self, *args, **kwargs):    
        # calculate the actual amount
        self.actual_amount = self.get_actual_amount()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Balance Owed Including VAT: ${self.total_amount} | Actual Amount: ${self.actual_amount}"
    class Meta:
        verbose_name = "Balance"
        verbose_name_plural = "Balances"