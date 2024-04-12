"""
Base App Forms
"""
from django import forms
from .models import Investment

class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['starting_amount', 'number_of_years', 'return_rate',
              'additional_contribution']
        