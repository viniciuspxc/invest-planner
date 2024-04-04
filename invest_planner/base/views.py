"""
Create Views for Base module
"""
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Investment
from .forms import InvestmentForm


# pylint: disable=too-many-ancestors
class InvestmentList(LoginRequiredMixin, ListView):
    """
    Main View: list of investments 
    """
    model = Investment
    context_object_name = 'investments'

    def get_queryset(self):
        return Investment.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = self.get_queryset().filter(active=True).count()
        search_input = self.request.GET.get('search_box') or ''
        if search_input:
            context['investments'] = context['investments'].filter(
                title__startswith=search_input)
        context['search_input'] = search_input
        return context


class InvestmentDetail(LoginRequiredMixin, DetailView):
    """
    View for checking investment details and calculations
    """
    model = Investment
    context_object_name = 'investment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        investment = self.get_object()
        number_of_years = getattr(investment, 'number_of_years', 0)
        starting_amount = getattr(investment, 'starting_amount', 0)
        return_rate = getattr(investment, 'return_rate', 0)

        total_result = starting_amount * \
            (1 + return_rate/100) ** number_of_years

        context['total_result'] = round(total_result, 2)
        return context


class InvestmentCreate(LoginRequiredMixin, CreateView):
    """
    View to form for investment creation
    """
    model = Investment
    fields = ['title', 'starting_amount', 'number_of_years', 'return_rate',
              'additional_contribution', 'active', 'starting_date', 'tags']
    # fields = ['title', 'starting_amount', 'number_of_years',
    #           'return_rate', 'additional_contribution', 'active', 'tags']
    success_url = reverse_lazy('investments')

    def form_valid(self, form):
        """
        Validade form and allow creation
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class InvestmentUpdate(LoginRequiredMixin, UpdateView):
    """
    View for editing investments
    """
    model = Investment
    fields = ['title', 'starting_amount', 'number_of_years', 'return_rate',
              'additional_contribution', 'active', 'starting_date', 'tags']
    success_url = reverse_lazy('investments')


class InvestmentDelete(LoginRequiredMixin, DeleteView):
    """
    View for deleting investments
    """
    model = Investment
    context_object_name = 'investment'
    success_url = reverse_lazy('investments')


class InvestmentFormView(LoginRequiredMixin, View):
    """
    View to form for a preview of investments
    """

    def get(self, request):
        """
        CRUD get
        """
        form = InvestmentForm()
        return render(request, 'base/investment_form.html', {'form': form})

    def post(self, request):
        """
        CRUD post
        """
        form = InvestmentForm(request.POST)

        if form.is_valid():
            total_result = form.cleaned_data['starting_amount']
            total_interest = 0
            yearly_results = {}

            for i in range(1, int(form.cleaned_data['number_of_years'] + 1)):
                yearly_results[i] = {}

                # Calculate the interest
                interest = total_result * \
                    (form.cleaned_data['return_rate'] / 100)
                total_result += interest
                total_interest += interest

                # Add additional contribution
                total_result += form.cleaned_data['annual_additional_contribution']

                # Set yearly results
                yearly_results[i]['interest'] = round(total_interest, 2)
                yearly_results[i]['total'] = round(total_result, 2)

            # Create context
            context = {
                'total_result': round(total_result, 2),
                'yearly_results': yearly_results,
                'number_of_years': int(form.cleaned_data['number_of_years'])
            }

            # Render the template
            return render(request, 'base/result.html', context)

        # Form is not valid, return bad request response
        return HttpResponseBadRequest("Form is not valid.")
