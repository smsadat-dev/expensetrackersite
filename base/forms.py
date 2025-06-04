from django import forms

from .models import ExpenseTrackerModel

class ExpenseTrackerForm(forms.ModelForm):
    class Meta:
        model = ExpenseTrackerModel
        fields = ['transaction_type', 'activity', 'value', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'})
        }