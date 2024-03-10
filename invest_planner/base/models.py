from datetime import date
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Tag(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class InvestmentTag(Tag):
    pass


class IncomeTag(Tag):
    pass


class ExpenseTag(Tag):
    pass


class Investment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=100, blank=True)
    starting_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal(0.00))
    number_of_years = models.IntegerField(default=0)
    return_rate = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal(0.00))
    additional_contribution = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal(0.00))
    active = models.BooleanField(default=True)
    starting_date = models.DateField(default=date.today)
    tags = models.ManyToManyField(
        InvestmentTag, related_name='investments', blank=True)

    def __str__(self):
        return f"{self.title} ({self.starting_amount})"


class Income(models.Model):
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
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, blank=True)
    monthly_expense = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal(0.00))
    tags = models.ManyToManyField(
        ExpenseTag, related_name='fixed_expenses', blank=True)

    def __str__(self):
        return f"{self.title} ({self.monthly_expense})"
