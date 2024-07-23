"""
Create Views for Base module
"""
from django.http import HttpResponseBadRequest
from django.db.models import Sum
from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Investment, Income, Expense, Tag
from .forms import InvestmentForm
from .models import InvestmentTag, IncomeTag, ExpenseTag
from .forms import InvestmentTagForm, IncomeTagForm, ExpenseTagForm

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

        monthly_income = Income.objects.aggregate(Sum('monthly_income'))[
            'monthly_income__sum'] or 0
        context['monthly_income'] = monthly_income

        monthly_expense = Expense.objects.aggregate(Sum('monthly_expense'))[
            'monthly_expense__sum'] or 0
        context['monthly_expense'] = monthly_expense
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
    template_name = 'base/investment_create.html'
    fields = ['title', 'starting_amount', 'number_of_years', 'return_rate',
              'additional_contribution', 'active', 'starting_date', 'tags']
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
    template_name = 'base/investment_create.html'
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


class InvestmentResults:
    """
    Represents the results of an investment calculation.
    """

    def __init__(self, total_result, yearly_results):
        self.total_result = total_result
        self.yearly_results = yearly_results


class InvestmentCalculator:
    """
    Handles the calculation of investment results.
    """

    @staticmethod
    def calculate_investment_results(form_data):
        total_result = form_data['starting_amount']
        total_interest = 0
        yearly_results = {}

        for i in range(1, int(form_data['number_of_years'] + 1)):
            yearly_results[i] = {}

            # Calculate the interest
            interest = total_result * (form_data['return_rate'] / 100)
            total_result += interest
            total_interest += interest

            # Add additional contribution
            total_result += form_data['additional_contribution']

            # Set yearly results
            yearly_results[i]['interest'] = round(total_interest, 2)
            yearly_results[i]['total'] = round(total_result, 2)

        return InvestmentResults(round(total_result, 2), yearly_results)


class InvestmentFormView(LoginRequiredMixin, View):
    """
    View to handle investment form submission and rendering.
    """

    def get(self, request):
        """
        Renders the investment form.
        """
        form = InvestmentForm()
        return render(request, 'base/investment_form.html', {'form': form})

    def post(self, request):
        """
        Handles form submission.
        """
        form = InvestmentForm(request.POST)

        if form.is_valid():
            form_data = form.cleaned_data
            investment_results = InvestmentCalculator.calculate_investment_results(
                form_data)

            context = {
                'form': form,
                'total_result': investment_results.total_result,
                'yearly_results': investment_results.yearly_results,
                'number_of_years': int(form_data['number_of_years'])
            }

            return render(request, 'base/investment_form.html', context)

        return HttpResponseBadRequest("Form is not valid.")


class IncomeList(LoginRequiredMixin, ListView):
    """
    Main View: list of incomes 
    """
    model = Income
    context_object_name = 'incomes'

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('search_box') or ''
        if search_input:
            context['incomes'] = context['incomes'].filter(
                title__startswith=search_input)
        context['search_input'] = search_input

        # monthly_income = Income.objects.aggregate(Sum('monthly_income'))['monthly_income__sum'] or 0
        # context['monthly_income'] = monthly_income

        return context


class IncomeCreate(LoginRequiredMixin, CreateView):
    """
    View to form for income creation
    """
    model = Income
    template_name = 'base/income_create.html'
    fields = ('title', 'monthly_income', 'tags')
    success_url = reverse_lazy('income-list')

    def form_valid(self, form):
        """
        Validade form and allow creation
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class IncomeUpdate(LoginRequiredMixin, UpdateView):
    """
    View for editing incomes
    """
    model = Income
    template_name = 'base/income_create.html'
    fields = ('title', 'monthly_income', 'tags')
    success_url = reverse_lazy('income-list')


class IncomeDelete(LoginRequiredMixin, DeleteView):
    """
    View for deleting incomes
    """
    model = Income
    context_object_name = 'income'
    success_url = reverse_lazy('income-list')


class ExpenseList(LoginRequiredMixin, ListView):
    """
    Main View: list of expenses 
    """
    model = Expense
    context_object_name = 'expenses'

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('search_box') or ''
        if search_input:
            context['expenses'] = context['expenses'].filter(
                title__startswith=search_input)
        context['search_input'] = search_input

        # monthly_expense = expense.objects.aggregate(Sum('monthly_expense'))['monthly_expense__sum'] or 0
        # context['monthly_expense'] = monthly_expense

        return context


class ExpenseCreate(LoginRequiredMixin, CreateView):
    """
    View to form for expense creation
    """
    model = Expense
    template_name = 'base/expense_create.html'
    fields = ('title', 'monthly_expense', 'tags')
    success_url = reverse_lazy('expense-list')

    def form_valid(self, form):
        """
        Validade form and allow creation
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class ExpenseUpdate(LoginRequiredMixin, UpdateView):
    """
    View for editing expenses
    """
    model = Expense
    template_name = 'base/expense_create.html'
    fields = ('title', 'monthly_expense', 'tags')
    success_url = reverse_lazy('expense-list')


class ExpenseDelete(LoginRequiredMixin, DeleteView):
    """
    View for deleting expenses
    """
    model = Expense
    context_object_name = 'expense'
    success_url = reverse_lazy('expense-list')


class TagListView(ListView):

    # def get_queryset(self):
    #     return {
    #         'investment_tags': InvestmentTag.objects.all(),
    #         'income_tags': IncomeTag.objects.all(),
    #         'expense_tags': ExpenseTag.objects.all()
    #     }
    """
    tags view 
    """
    template_name = 'tags/tag_list.html'

    def get_queryset(self):
        return {
            'investment_tags': InvestmentTag.objects.all(),
            'income_tags': IncomeTag.objects.all(),
            'expense_tags': ExpenseTag.objects.all(),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {
            'investment_tags': InvestmentTag.objects.all(),
            'income_tags': IncomeTag.objects.all(),
            'expense_tags': ExpenseTag.objects.all(),
        }
        tags = Tag.objects.all()
        context['tags'] = tags
        return context


class InvestmentTagCreateView(CreateView):
    model = InvestmentTag
    form_class = InvestmentTagForm
    template_name = 'tags/tag_form.html'
    success_url = reverse_lazy('tag-list')


class InvestmentTagUpdateView(UpdateView):
    model = InvestmentTag
    form_class = InvestmentTagForm
    template_name = 'tags/tag_form.html'
    success_url = reverse_lazy('tag-list')


class InvestmentTagDeleteView(DeleteView):
    model = InvestmentTag
    template_name = 'tags/tag_confirm_delete.html'
    success_url = reverse_lazy('tag-list')


class IncomeTagCreateView(CreateView):
    model = IncomeTag
    form_class = IncomeTagForm
    template_name = 'tags/tag_form.html'
    success_url = reverse_lazy('tag-list')


class IncomeTagUpdateView(UpdateView):
    model = IncomeTag
    form_class = IncomeTagForm
    template_name = 'tags/tag_form.html'
    success_url = reverse_lazy('tag-list')


class IncomeTagDeleteView(DeleteView):
    model = IncomeTag
    template_name = 'tags/tag_confirm_delete.html'
    success_url = reverse_lazy('tag-list')


class ExpenseTagCreateView(CreateView):
    model = ExpenseTag
    form_class = ExpenseTagForm
    template_name = 'tags/tag_form.html'
    success_url = reverse_lazy('tag-list')


class ExpenseTagUpdateView(UpdateView):
    model = ExpenseTag
    form_class = ExpenseTagForm
    template_name = 'tags/tag_form.html'
    success_url = reverse_lazy('tag-list')


class ExpenseTagDeleteView(DeleteView):
    model = ExpenseTag
    template_name = 'tags/tag_confirm_delete.html'
    success_url = reverse_lazy('tag-list')
