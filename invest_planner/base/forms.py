"""
Base App Forms
"""
from django import forms
from .models import Investment

# class InvestmentForm(forms.ModelForm):
#     class Meta:
#         model = Investment
#         fields = ['starting_amount', 'number_of_years', 'return_rate',
#               'additional_contribution']
#         # fields = ['title', 'starting_amount', 'number_of_years', 'return_rate',
#         #           'additional_contribution', 'active', 'starting_date', 'tags']

class InvestmentForm(forms.Form):
    """
    InvestmentForm 
    """
    starting_amount = forms.FloatField()
    number_of_years = forms.FloatField()
    return_rate = forms.FloatField()
    additional_contribution = forms.FloatField()
