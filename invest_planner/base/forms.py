"""
Base App Forms
"""
from django import forms
from .models import InvestmentTag, IncomeTag, ExpenseTag
from .models import Investment


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
        fields = ['title', 'starting_amount', 'number_of_years', 'investment_type',
                  'return_rate', 'rate_type', 'rate_percentage',
                  'additional_contribution', 'active', 'starting_date', 'tags']

    def clean(self):
        cleaned_data = super().clean()
        investment_type = cleaned_data.get('investment_type')
        rate_percentage = cleaned_data.get('rate_percentage')
        if investment_type == 'pos' and rate_percentage is None:
            self.add_error(
                'rate_percentage', 'Por favor, forneça a porcentagem da taxa para investimentos pós-fixados.')
        return cleaned_data


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
