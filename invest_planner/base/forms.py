"""
Base App Forms
"""
from django import forms
from .models import InvestmentTag, IncomeTag, ExpenseTag
from .models import Investment
from .utils import get_central_bank_rate
from datetime import date


class InvestmentForm(forms.ModelForm):
    starting_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'value': date.today,
            }
        )
    )

    rate_type = forms.ChoiceField(choices=[('', '------')], required=False)

    class Meta:
        model = Investment
        fields = ['title', 'starting_amount', 'number_of_years',
                  'return_rate', 'rate_type',  'rate_value', 'rate_percentage',
                  'additional_contribution', 'active', 'starting_date', 'tags']

    def __init__(self, *args, **kwargs):
        super(InvestmentForm, self).__init__(*args, **kwargs)
        central_bank_rates = get_central_bank_rate()
        rate_choices = [(tax['name'], f"{tax['name'].upper()} ({
                         tax['rate']}%)") for tax in central_bank_rates['taxes']
                        ]
        self.fields['rate_type'].choices += rate_choices
        self.fields['rate_value'].widget.attrs['readonly'] = False
        self.fields['rate_percentage'].widget.attrs['readonly'] = False


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
