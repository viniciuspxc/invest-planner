"""
Define URLs for Base module
"""
from django.urls import path
from .views import InvestmentList, InvestmentDetail
from .views import InvestmentCreate, InvestmentUpdate, InvestmentDelete
from .views import IncomeList, IncomeCreate, IncomeUpdate, IncomeDelete
from .views import ExpenseList, ExpenseCreate, ExpenseUpdate, ExpenseDelete
# from .views import TagCreate, TagUpdate, TagDelete
from .views import InvestmentFormView
from .views import (
    TagListView,
    InvestmentTagCreateView, InvestmentTagUpdateView, InvestmentTagDeleteView,
    IncomeTagCreateView, IncomeTagUpdateView, IncomeTagDeleteView,
    ExpenseTagCreateView, ExpenseTagUpdateView, ExpenseTagDeleteView
)
from .views import InvestmentRatesView

urlpatterns = [
    path('', InvestmentList.as_view(), name='investments'),
    path('investment/<int:pk>/', InvestmentDetail.as_view(), name='investment'),
    path('investment-create/', InvestmentCreate.as_view(),
         name='investment-create'),
    path('investment-update/<int:pk>/',
         InvestmentUpdate.as_view(), name='investment-update'),
    path('investment-delete/<int:pk>/',
         InvestmentDelete.as_view(), name='investment-delete'),
    path('investment-form/', InvestmentFormView.as_view(),
         name='investment-form'),

    path('income-list/', IncomeList.as_view(), name='income-list'),
    path('income-create/', IncomeCreate.as_view(),
         name='income-create'),
    path('income-update/<int:pk>/',
         IncomeUpdate.as_view(), name='income-update'),
    path('income-delete/<int:pk>/',
         IncomeDelete.as_view(), name='income-delete'),

    path('expense-list/', ExpenseList.as_view(), name='expense-list'),
    path('expense-create/', ExpenseCreate.as_view(),
         name='expense-create'),
    path('expense-update/<int:pk>/',
         ExpenseUpdate.as_view(), name='expense-update'),
    path('expense-delete/<int:pk>/',
         ExpenseDelete.as_view(), name='expense-delete'),

    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tags/investment/create/', InvestmentTagCreateView.as_view(), name='investmenttag-create'),
    path('tags/investment/update/<int:pk>/', InvestmentTagUpdateView.as_view(), name='investmenttag-update'),
    path('tags/investment/delete/<int:pk>/', InvestmentTagDeleteView.as_view(), name='investmenttag-delete'),
    path('tags/income/create/', IncomeTagCreateView.as_view(), name='incometag-create'),
    path('tags/income/update/<int:pk>/', IncomeTagUpdateView.as_view(), name='incometag-update'),
    path('tags/income/delete/<int:pk>/', IncomeTagDeleteView.as_view(), name='incometag-delete'),
    path('tags/expense/create/', ExpenseTagCreateView.as_view(), name='expensetag-create'),
    path('tags/expense/update/<int:pk>/', ExpenseTagUpdateView.as_view(), name='expensetag-update'),
    path('tags/expense/delete/<int:pk>/', ExpenseTagDeleteView.as_view(), name='expensetag-delete'),
    
    path('investment-rates/', InvestmentRatesView.as_view(), name='investment-rates'),
]
