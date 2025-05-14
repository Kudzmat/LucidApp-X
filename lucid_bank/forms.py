from django import forms

BANK_CHOICES = [
    ('saman', 'Saman'),
    ('lucidity', 'Lucidity'),
    ('other', 'Other'),
]


class WithdrawalForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    transaction = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'ATM withdrawal, cash out...'}))
    debit = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Amount to withdraw'}))
    bank = forms.ChoiceField(choices=BANK_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select bank to withdaw from'}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional notes'}))


class PaymentForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    transaction = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Payment for order, supplier...'}))
    debit = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Amount to pay'}))
    bank = forms.ChoiceField(choices=BANK_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select bank to pay to'}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional notes'}))


class TransferForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    transaction = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Transfer between accounts'}))
    debit = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Amount sent'}))
    credit = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Amount received'}))
    bank = forms.ChoiceField(choices=BANK_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select bank to transfer to'}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional notes'}))

