from django.db import models

# Create your models here.
class Saman(models.Model):
    date = models.DateField(blank=False, null=False)
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
            return f"{self.date} - Debit: {self.debit} | {self.transaction}"
        elif self.credit > 0:
            return f"{self.date} - Credit: {self.credit} | {self.transaction}"
        else:
            return "No transaction"
  
class LucidBank(models.Model):
    date = models.DateField(blank=False, null=False)
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
            return f"{self.date} - Debit: {self.debit} | {self.transaction}"
        elif self.credit > 0:
            return f"{self.date} - Credit: {self.credit} | {self.transaction}"
        else:
            return "No transaction"