"""
Base App Forms
"""
from datetime import date
from django import forms
from .models import InvestmentTag, IncomeTag, ExpenseTag
from .models import Investment
from .utils import get_central_bank_rate


class InvestmentForm(forms.ModelForm):
    """Formulário para cofigurar o cadastro de investimentos
    """
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
        super().__init__(*args, **kwargs)
        central_bank_rates = get_central_bank_rate()
        rate_choices = [(tax['name'], f"{tax['name'].upper()} ({
                         tax['rate']}%)") for tax in central_bank_rates['taxes']
                        ]
        self.fields['rate_type'].choices += rate_choices
        self.fields['rate_value'].widget.attrs['readonly'] = False
        self.fields['rate_percentage'].widget.attrs['readonly'] = False


class InvestmentTagForm(forms.ModelForm):
    """Formulário para tags de investimento
    """
    class Meta:
        model = InvestmentTag
        fields = ['name']


class IncomeTagForm(forms.ModelForm):
    """Formulário para tags de ganhos
    """
    class Meta:
        model = IncomeTag
        fields = ['name']


class ExpenseTagForm(forms.ModelForm):
    """Formulário para tags de gastos
    """
    class Meta:
        model = ExpenseTag
        fields = ['name']
