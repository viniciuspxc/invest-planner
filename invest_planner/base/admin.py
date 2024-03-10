from django.contrib import admin
from .models import *

admin.site.register(Tag)
admin.site.register(InvestmentTag)
admin.site.register(IncomeTag)
admin.site.register(ExpenseTag)
admin.site.register(Investment)
admin.site.register(Income)
admin.site.register(Expense)