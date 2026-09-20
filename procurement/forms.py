from django import forms
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import PurchaseRequest

class PurchaseRequestForm(forms.ModelForm):
    class Meta:
        model = PurchaseRequest
        fields = ['item_name', 'estimated_cost', 'justification']
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item or service name'}),
            'estimated_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'justification': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Business rationale'}),
        }

    def clean_item_name(self):
        name = self.cleaned_data.get('item_name', '').strip()
        if len(name) < 3:
            raise ValidationError("Item name must be at least 3 characters long.")
        return name

    def clean_estimated_cost(self):
        cost = self.cleaned_data.get('estimated_cost')
        if cost is None or cost <= Decimal('0.00'):
            raise ValidationError("Estimated cost must be greater than $0.00.")
        if cost > Decimal('100000.00'):
            raise ValidationError("Orders above $100,000.00 require executive board approval.")
        return cost

    def clean_justification(self):
        justification = self.cleaned_data.get('justification', '').strip()
        if len(justification) < 5:
            raise ValidationError("Please provide a meaningful justification (at least 5 characters).")
        return justification