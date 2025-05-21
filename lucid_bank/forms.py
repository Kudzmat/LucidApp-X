from django import forms

BANK_CHOICES = [
    ('saman', 'Saman'),
    ('lucidity', 'Lucidity'),
    ('other', 'Other'),
]


class WithdrawalForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    transaction = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'ATM withdrawal, cash out...'}))
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Amount to withdraw'}))
    withdraw_from = forms.ChoiceField(choices=BANK_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select bank to withdaw from'}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional notes'}))


class PaymentForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    transaction = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Payment for order, supplier...'}))
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Amount to pay'}))
    pay_to = forms.ChoiceField(choices=BANK_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select bank to pay to'}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional notes'}))


class TransferForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    transaction = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Transfer between accounts'}))
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Amount sent'}))
    pay_to = forms.ChoiceField(choices=BANK_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select bank to transfer to'}))
    pay_from = forms.ChoiceField(choices=BANK_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select bank to pay from'}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional notes'}))

