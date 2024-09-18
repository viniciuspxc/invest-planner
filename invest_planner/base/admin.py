"""
Admin file to register Models to Django Admin interface
"""
from django.contrib import admin
from .models import Tag, Investment, InvestmentTag, Income, IncomeTag, Expense, ExpenseTag, Notification


admin.site.register(Tag)
admin.site.register(InvestmentTag)
admin.site.register(IncomeTag)
admin.site.register(Investment)
admin.site.register(ExpenseTag)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(Notification)
