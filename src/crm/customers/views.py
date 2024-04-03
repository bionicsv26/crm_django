from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, DetailView, DeleteView

from .forms import CustomerForm
from .models import Customer
from ..contracts.views import get_data_for_form


class CustomerListView(PermissionRequiredMixin, ListView):
    """Класс для отображения списка покупателей."""

    permission_required = "customers.view_customer"
    model = Customer
    template_name = 'customers/customers-list.html'
    context_object_name = 'customers'


class CustomerDetailView(PermissionRequiredMixin, DetailView):
    """Класс для детального отображения покупателя."""

    permission_required = "customers.view_customer"
    model = Customer
    template_name = 'customers/customers-detail.html'


class CustomerCreateView(PermissionRequiredMixin, View):
    """Класс для создания покупателя."""

    permission_required = "customers.add_customer"
    template_name = 'customers/customers-create.html'
    success_url = reverse_lazy('crm.customers:customers_list')

    def get(self, request):
        """
        Метод get проверяет есть ли в кэше параметр lead_id:
        если есть, то выдает форму с предзаполнеными данными,
        иначе выдает пустую.
        """
        dict_data_for_form = get_data_for_form()
        if dict_data_for_form is not None:
            form = CustomerForm(data=dict_data_for_form)
        else:
            form = CustomerForm()

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Метод post сохраняет форму при ее валидности иначе возвращает форму с ошибками."""
        form = CustomerForm(request.POST)

        with transaction.atomic():
            if form.is_valid():
                lead = form.cleaned_data['lead']
                lead.to_active = True
                lead.save()
                form.save()
                return redirect(self.success_url)

        return render(request, self.template_name, {'form': form})


class CustomerUpdateView(PermissionRequiredMixin, UpdateView):
    """Класс для обновления данных покупателя."""

    permission_required = "customers.change_customer"
    model = Customer
    template_name = 'customers/customers-edit.html'
    fields = '__all__'
    success_url = reverse_lazy('crm.customers:customers_list')


class CustomerDeleteView(PermissionRequiredMixin, DeleteView):
    """Класс для удаления покупателя."""

    permission_required = "customers.delete_customer"
    model = Customer
    template_name = 'customers/customers-delete.html'
    success_url = reverse_lazy('crm.customers:customers_list')
