from django.forms import BaseModelForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task, Investment
from .forms import InvestmentForm


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search_box') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__startswith=search_input)

        context['search_input'] = search_input
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class Taskupdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    
class InvestmentFormView(LoginRequiredMixin, View):
	def get(self, request):
		form = InvestmentForm()
		return render(request, 'base/investment_form.html', {'form': form})

	def post(self, request):
		form = InvestmentForm(request.POST)

		if form.is_valid():
			total_result = form.cleaned_data['starting_amount']
			total_interest = 0
			yearly_results = {}

			for i in range(1, int(form.cleaned_data['number_of_years'] + 1)):
				yearly_results[i] = {}

				# calculate the interest
				interest = total_result * (form.cleaned_data['return_rate'] / 100)
				total_result += interest
				total_interest += interest

				# add additional contribution
				total_result += form.cleaned_data['annual_additional_contribution']

				# set yearly_results
				yearly_results[i]['interest'] = round(total_interest, 2)
				yearly_results[i]['total'] = round(total_result, 2)

				# create context
				context = {
					'total_result': round(total_result, 2),
					'yearly_results': yearly_results,
					'number_of_years': int(form.cleaned_data['number_of_years'])
				}

			# render the template
			return render(request, 'base/result.html', context)


class InvestmentCreate(LoginRequiredMixin, CreateView):
    model = Investment
    fields = ['title', 'starting_amount', 'number_of_years',
              'return_rate', 'annual_additional_contribution']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(InvestmentCreate, self).form_valid(form)
