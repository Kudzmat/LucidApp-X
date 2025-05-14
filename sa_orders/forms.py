from django import forms
from .models import SaOrder

COMPANY_CHOICES = [
    ('adendorff', 'Adendorff'),
    ('chemvulc', 'Chemvulc'),
    ('academy', 'Academy'),
    ('tools_wholesale', 'Tools Wholesale'),
    ('resolute_supplies', 'Resolute Supplies'),
    ('other', 'Other'),
]

class SaOrderForm(forms.ModelForm):
    companies = forms.MultipleChoiceField(
        choices=COMPANY_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = SaOrder
        exclude = [
            'usd_amount',
            'internal_bank_deduction',
            'total_cost',
            'revenue',
            'revenue_vat',
            'profit',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'zar_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'my_zar_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'client_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'markup': forms.NumberInput(attrs={'class': 'form-control'}),
            'pick_up_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'transport_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'delivery_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
