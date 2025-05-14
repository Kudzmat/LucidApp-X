from django import forms
from .models import LocalOrder

class LocalOrderForm(forms.ModelForm):
    class Meta:
        model = LocalOrder
        fields = ['date', 'amount', 'markup', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter order amount in USD'}),
            'markup': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter markup percentage'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter any additional notes'}),
        }
        labels = {
            'date': 'Order Date',
            'amount': 'Order Amount (USD)',
            'markup': 'Markup (%)',
            'notes': 'Additional Notes',
        }
        help_texts = {
            'amount': 'The cost of the order in USD.',
            'markup': 'The markup percentage to apply to the order.',
        }