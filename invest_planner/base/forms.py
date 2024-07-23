"""
Base App Forms
"""
from django import forms
from .models import Investment
from .models import InvestmentTag, IncomeTag, ExpenseTag


class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['starting_amount', 'number_of_years', 'return_rate',
                  'additional_contribution']


class InvestmentTagForm(forms.ModelForm):
    class Meta:
        model = InvestmentTag
        fields = ['name']


class IncomeTagForm(forms.ModelForm):
    class Meta:
        model = IncomeTag
        fields = ['name']


class ExpenseTagForm(forms.ModelForm):
    class Meta:
        model = ExpenseTag
        fields = ['name']
