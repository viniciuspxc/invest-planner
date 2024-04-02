from django.urls import path
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # path('accounts/logout/', LogoutView.as_view(next_page='/accounts/login'),
    #      name='account_logout'),
]

