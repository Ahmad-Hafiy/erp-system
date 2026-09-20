from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import LeaveRequest, ExpenseClaim, LeaveBalance

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['start_date', 'end_date', 'days_requested', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'days_requested': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        days = cleaned_data.get('days_requested')

        if start and end:
            if end < start:
                raise ValidationError("End date cannot be earlier than start date.")
            if start < timezone.now().date():
                raise ValidationError("Start date cannot be in the past.")

        if days and self.user:
            balance, _ = LeaveBalance.objects.get_or_create(user=self.user)
            if days > balance.remaining_days:
                raise ValidationError(
                    f"Requested {days} days, but you only have {balance.remaining_days} days remaining."
                )

        return cleaned_data


class ExpenseClaimForm(forms.ModelForm):
    class Meta:
        model = ExpenseClaim
        fields = ['title', 'amount', 'receipt']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'receipt': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_receipt(self):
        file = self.cleaned_data.get('receipt')
        if not file:
            return file

        allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
        name_lower = file.name.lower()
        if not any(name_lower.endswith(ext) for ext in allowed_extensions):
            raise ValidationError("Allowed file types: PDF, PNG, JPG, JPEG.")

        max_size = 5 * 1024 * 1024  # 5 MB limit
        if file.size > max_size:
            raise ValidationError("File size exceeds the 5MB limit.")

        return file