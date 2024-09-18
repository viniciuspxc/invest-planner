"""
Create Views for Base module
"""
from decouple import config
from groq import Groq
from .models import Investment, Income, Expense
import json
import openai
from django.http import JsonResponse
from decimal import Decimal
from datetime import date, datetime
from django.db.models import Q, Sum
from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, When, Value, IntegerField
from .models import Investment, Income, Expense, Tag
from .models import InvestmentTag, IncomeTag, ExpenseTag
from .forms import InvestmentTagForm, IncomeTagForm, ExpenseTagForm
from .forms import InvestmentForm
from .utils import get_central_bank_rate, get_user_data

# pylint: disable=too-many-ancestors


class InvestmentList(LoginRequiredMixin, ListView):
    """
    Main View: list of investments
    """
    model = Investment
    context_object_name = 'investments'

    def get_queryset(self):
        """
        Returns investments filtered by the current user, ordered by
        active status (active first) and then by starting_date (latest first).
        """
        queryset = Investment.objects.filter(user=self.request.user)
        queryset = queryset.order_by(
            Case(
                When(active=True, then=Value(0)),
                default=Value(1),
                output_field=IntegerField()
            ),
            '-starting_date'
        )

        search_input = self.request.GET.get('search_box') or ''
        if search_input:
            queryset = queryset.filter(
                Q(title__icontains=search_input) | Q(
                    tags__name__icontains=search_input)
            ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = self.get_queryset().filter(active=True).count()
        search_input = self.request.GET.get('search_box') or ''
        context['search_input'] = search_input

        total_investment_value = Investment.objects.filter(user=self.request.user).aggregate(
            Sum('starting_amount'))['starting_amount__sum'] or 0
        context['total_investment_value'] = total_investment_value

        monthly_income = Income.objects.filter(user=self.request.user).aggregate(
            Sum('monthly_income'))['monthly_income__sum'] or 0
        context['monthly_income'] = monthly_income

        monthly_expense = Expense.objects.filter(user=self.request.user).aggregate(
            Sum('monthly_expense'))['monthly_expense__sum'] or 0
        context['monthly_expense'] = monthly_expense

        for investment in context['investments']:
            investment.total_monthly_income = investment.calculate_monthly_income()
            investment.end_date = investment.calculate_end_date()

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

        return_rate = getattr(investment, 'return_rate', Decimal('0.00'))
        rate_percentage = getattr(
            investment, 'rate_percentage', Decimal('0.00'))
        rate_value = getattr(investment, 'rate_value', Decimal('0.00'))

        months = []
        total_amount = getattr(investment, 'starting_amount', Decimal('0.00'))
        current_date = getattr(
            investment, 'starting_date', datetime.today().date()).replace(day=1)

        for _ in range(getattr(investment, 'number_of_years', 0) * 12):
            fixed_return = total_amount * return_rate / \
                Decimal('100') / Decimal('12')

            if getattr(investment, 'rate_type') and rate_percentage and rate_value:
                variable_return = total_amount * \
                    (rate_value * rate_percentage / Decimal('100')) / \
                    Decimal('100') / Decimal('12')
            else:
                variable_return = Decimal('0.00')

            total_monthly_income = fixed_return + variable_return + getattr(
                investment, 'additional_contribution', Decimal('0.00'))
            total_amount += total_monthly_income

            months.append({
                'date': current_date,
                'monthly_income': round(total_monthly_income, 2),
                'total_value': round(total_amount, 2),
            })

            if current_date.month >= 12:
                current_date = current_date.replace(
                    year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(
                    month=current_date.month + 1)

        context['months'] = months
        context['total_result'] = round(total_amount, 2)

        return context


class InvestmentCreate(LoginRequiredMixin, CreateView):
    model = Investment
    template_name = 'base/investment_create.html'
    form_class = InvestmentForm
    success_url = reverse_lazy('investments')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_central_bank_rate())
        return context

    def form_valid(self, form):
        """
        Valida o formulário
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class InvestmentUpdate(LoginRequiredMixin, UpdateView):
    model = Investment
    template_name = 'base/investment_create.html'
    form_class = InvestmentForm
    success_url = reverse_lazy('investments')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_central_bank_rate())
        return context

    def form_valid(self, form):
        """
        Valida o formulário
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class InvestmentDelete(LoginRequiredMixin, DeleteView):
    """
    View for deleting investments
    """
    model = Investment
    context_object_name = 'investment'
    success_url = reverse_lazy('investments')


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


class InvestmentRatesView(View):
    def get(self, request):
        context = get_central_bank_rate()
        return render(request, 'base/investment_rates.html', context)


def UserDataView(request):
    user = request.user
    customer_data = get_user_data(user)

    return render(request, 'base/summarize.html', {'customer_data': json.dumps(customer_data, indent=4)})


GROQ_API_KEY = config('GROQ_API_KEY')
client = Groq(api_key=GROQ_API_KEY)  # type: ignore


def chat_with_assistant(message, user):
    json_data = get_user_data(user)

    try:
        completion = client.chat.completions.create(
            model="llama3-groq-70b-8192-tool-use-preview",
            messages=[
                {
                    "role": "system",
                    "content": f"User data is in the json: {json_data}; Don't use formulas or codes; Calculate the values if asked; Use less than 100 words; Make sure calculations are correct"
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0.2,
            max_tokens=200,
            top_p=0.65,
            stream=False,
            stop=None,
        )

        # Acesso ao conteúdo da resposta com base na documentação
        if hasattr(completion, 'choices') and len(completion.choices) > 0:
            # Assumindo que `message` está disponível diretamente no objeto
            response_message = completion.choices[0].message
            if hasattr(response_message, 'content'):
                return response_message.content
            else:
                return "Content not found in response."
        else:
            return "No choices available in response."

    except Exception as e:
        # Lidar com erros e exceções
        return f"An error occurred: {str(e)}"


# View para o chatbot
def chatbot_view(request):
    user = request.user
    if request.method == 'POST':
        user_message = request.POST.get('message')
        bot_response = chat_with_assistant(user_message, user)
        return JsonResponse({'response': bot_response})
    return render(request, 'base/chatbot.html')
