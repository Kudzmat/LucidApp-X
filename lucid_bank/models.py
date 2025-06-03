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
    date = models.DateTimeField(default=now, null=True, blank=True)
    transaction = models.CharField(max_length=255, blank=False, null=True)
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=True,
        help_text="The total VAT amount owed by suppliers"
    )

    actual_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=True,
        help_text="The actual amount owed by suppliers"
    )

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

    # The amount Lucidity will take is calculated using this method
    def get_actual_balance(self):
        vat = Decimal(1.15)
        less_vat = self.balance / vat
        # calculate amount with 3% bank withdrawal charge
        bank_charge = Decimal(1.03)
        actual_balance = Decimal(less_vat / bank_charge)
        return actual_balance
    
    def save(self, *args, **kwargs):    
        # calculate the actual amount
        self.actual_balance = self.get_actual_balance()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Balance Owed Including VAT: ${self.balance} | Actual Amount: ${self.actual_balance}"
    class Meta:
        verbose_name = "Balance Owed"
        verbose_name_plural = "Balances owed"