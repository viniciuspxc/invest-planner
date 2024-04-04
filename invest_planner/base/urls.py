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
]
