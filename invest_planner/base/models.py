"""
Models for Base App module
"""
from datetime import date
from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    """
    Tag model
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class InvestmentTag(Tag):
    """
    InvestmentTag extends Tag
    """


class IncomeTag(Tag):
    """
    IncomeTag extends Tag
    """


class ExpenseTag(Tag):
    """
    ExpenseTag extends Tag
    """


class Investment(models.Model):
    """
    Investment model to save into database
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, blank=True, default="inv")
    starting_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal(0.00))
    number_of_years = models.IntegerField(default=0)
    return_rate = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal(0.00))
    additional_contribution = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal(0.00))
    rate_type = models.CharField(
        max_length=5, blank=True, null=True)
    rate_value = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, default=Decimal(0.00))
    rate_percentage = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, default=Decimal(0.00))
    active = models.BooleanField(default=True)
    starting_date = models.DateField(default=date.today)
    tags = models.ManyToManyField(
        InvestmentTag, related_name='investments', blank=True)

    def __str__(self):
        return f"{self.title} ({self.starting_amount})"

    def calculate_monthly_income(self):
        """
        Calcula o ganho mensal com base no return_rate e rate_percentage.
        """

        starting_amount = self.starting_amount
        return_rate = self.return_rate
        rate_percentage = self.rate_percentage
        rate_value = self.rate_value

        fixed_return = starting_amount * return_rate / Decimal('100')

        if self.rate_type == 'CDI':
            variable_return = starting_amount * \
                (rate_value * rate_percentage / Decimal('100')) / Decimal('100')
        elif self.rate_type == 'SELIC':
            variable_return = starting_amount * \
                (rate_value * rate_percentage / Decimal('100')) / Decimal('100')
        else:
            variable_return = Decimal('0.00')

        total_monthly_income = fixed_return + \
            variable_return + self.additional_contribution
        return total_monthly_income


class Income(models.Model):
    """
    Income model to save into database
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, blank=True)
    monthly_income = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal(0.00))
    tags = models.ManyToManyField(
        IncomeTag, related_name='fixed_incomes', blank=True)

    def __str__(self):
        return f"{self.title} ({self.monthly_income})"


class Expense(models.Model):
    """
    Expenses model to save into database
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, blank=True)
    monthly_expense = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal(0.00))
    tags = models.ManyToManyField(
        ExpenseTag, related_name='fixed_expenses', blank=True)

    def __str__(self):
        return f"{self.title} ({self.monthly_expense})"
