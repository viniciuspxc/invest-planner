"""
Base App Forms
"""
from django import forms
from .models import Investment
from .models import InvestmentTag, IncomeTag, ExpenseTag


class InvestmentForm(forms.ModelForm):
    starting_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date'
            }
        )
    )

    class Meta:
        model = Investment
        fields = ['title', 'starting_amount', 'number_of_years', 'return_rate',
                  'additional_contribution', 'active', 'starting_date', 'tags']


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
