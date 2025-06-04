from decimal import Decimal

from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.db.models import Sum

from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView

from .forms import ExpenseTrackerForm
from .models import ExpenseTrackerModel


# Expense tracker views

class ExpenseTrackerListView(ListView):
    model = ExpenseTrackerModel
    context_object_name = 'list'
    form_class = ExpenseTrackerForm
    template_name = 'base/showexpense.html'
    success_url = reverse_lazy('base:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = kwargs.get('form', self.form_class())

        # <--- CALCULATE TOTAL BALANCE ---
        total_value = ExpenseTrackerModel.objects.aggregate(total_sum=Sum('value'))['total_sum']
        context['total_balance'] = total_value if total_value is not None else Decimal('0.00')
        # --- Calculate Total Income ---
        total_income = ExpenseTrackerModel.objects.filter(transaction_type='income').aggregate(total_sum=Sum('value'))['total_sum']
        context['total_income'] = total_income if total_income is not None else Decimal('0.00')
        # --- Calculate Total Expense ---
        total_expense = ExpenseTrackerModel.objects.filter(transaction_type='expense').aggregate(total_sum=Sum('value'))['total_sum']
        context['total_expense'] = total_expense if total_expense is not None else Decimal('0.00')
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
            
        
    def form_valid(self, form):
        instance = form.instance

        if instance.transaction_type == 'expense':
            instance.value = -abs(instance.value)

        else:   
            instance.value = abs(instance.value)

        form.save()
        success_url = reverse_lazy('base:home')
        return HttpResponseRedirect(success_url) 
    
    def form_invalid(self, form):
        context = self.get_context_data()
        return self.render_to_response(context)

ExpenTrackListView = ExpenseTrackerListView.as_view()


class ExpenseTrackerDetailView(DetailView):
    model = ExpenseTrackerModel
    template_name = 'base/showexpense.html'
    context_object_name = 'expense'

class ExpenseTrackerDeleteView(DeleteView):
    model = ExpenseTrackerModel
    success_url = reverse_lazy('base:home')