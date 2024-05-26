from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView, View

from .forms import LeadForm
from .models import Lead


class LeadListView(PermissionRequiredMixin, ListView):
    """Класс для отображения списка потенциальных клиентов."""

    permission_required = "leads.view_lead"
    queryset = Lead.objects.filter(to_active=False)
    template_name = 'leads/leads-list.html'
    context_object_name = 'leads'


class LeadDetailView(PermissionRequiredMixin, DetailView):
    """Класс для детального отображения потенциального клиента."""

    permission_required = "leads.view_lead"
    model = Lead
    template_name = 'leads/leads-detail.html'


class LeadCreateView(PermissionRequiredMixin, CreateView):
    """Класс для создания потенциального клиента."""

    permission_required = "leads.add_lead"
    form_class = LeadForm
    template_name = 'leads/leads-create.html'
    success_url = reverse_lazy('crm.leads:leads_list')


class LeadUpdateView(PermissionRequiredMixin, UpdateView):
    """Класс для обновления данных потенциального клиента."""

    permission_required = "leads.change_lead"
    model = Lead
    template_name = 'leads/leads-edit.html'
    fields = '__all__'
    success_url = reverse_lazy('crm.leads:leads_list')


class LeadDeleteView(PermissionRequiredMixin, DeleteView):
    """Класс для удаления потенциального клиента."""

    permission_required = "leads.delete_lead"
    model = Lead
    template_name = 'leads/leads-delete.html'
    success_url = reverse_lazy('crm.leads:leads_list')


class LeadTransferToActiveView(PermissionRequiredMixin, View):
    """Класс для перевода потенциальных клиентов в активные."""

    permission_required = "leads.can_transfer_to_active"

    def get(self, request, *args, **kwargs):
        """Метод get сохраняет в кэш значение lead_id и запускает создание покупателя"""
        cache.set('lead_id', kwargs['pk'], timeout=5)
        return HttpResponseRedirect(reverse_lazy('crm.customers:customers_create'))


class LeadTransferToContractView(PermissionRequiredMixin, View):
    """Класс для создания контракта на основании потенциального клиента."""

    permission_required = "contracts.add_contract"

    def get(self, request, *args, **kwargs):
        """Метод get сохраняет в кэш значение lead_id и запускает создание контракта"""
        cache.set('lead_id', kwargs['pk'], timeout=5)
        return HttpResponseRedirect(reverse_lazy('crm.contracts:contract_create'))
