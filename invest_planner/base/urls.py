"""
Define URLs for Base module
"""
from django.urls import path
from .views import InvestmentList, InvestmentDetail
from .views import InvestmentCreate, InvestmentUpdate, InvestmentDelete
from .views import InvestmentFormView

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

#     path('', incomeList.as_view(), name='incomes'),
#     path('income/<int:pk>/', incomeDetail.as_view(), name='income'),
#     path('income-create/', incomeCreate.as_view(),
#          name='income-create'),
#     path('income-update/<int:pk>/',
#          incomeUpdate.as_view(), name='income-update'),
#     path('income-delete/<int:pk>/',
#          incomeDelete.as_view(), name='income-delete'),
#     path('income-form/', incomeFormView.as_view(),
#          name='income-form'),
]
