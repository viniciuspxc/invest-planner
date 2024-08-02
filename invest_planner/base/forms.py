"""
Base App Forms
"""
from django import forms
from .models import InvestmentTag, IncomeTag, ExpenseTag
from .models import Investment
from .utils import get_central_bank_rate


class InvestmentForm(forms.ModelForm):
    starting_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date'
            }
        )
    )

    rate_type = forms.ChoiceField(choices=[('', '------')], required=False)
    rate_percentage = forms.DecimalField(max_digits=5, decimal_places=2, required=False, initial=0)

    class Meta:
        model = Investment
        fields = ['title', 'starting_amount', 'number_of_years',
                  'return_rate', 'rate_type', 'rate_percentage',
                  'additional_contribution', 'active', 'starting_date', 'tags']

    def __init__(self, *args, **kwargs):
        super(InvestmentForm, self).__init__(*args, **kwargs)
        central_bank_rates = get_central_bank_rate()
        rate_choices = [(tax['name'], f"{tax['name'].upper()} ({tax['rate']}%)") for tax in central_bank_rates['taxes']]
        self.fields['rate_type'].choices += rate_choices
        # Initialize rate_percentage to 0 and set it as inaccessible if rate_type is empty
        self.fields['rate_percentage'].widget.attrs['readonly'] = True


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
