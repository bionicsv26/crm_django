from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, DetailView, DeleteView

from .forms import ContractForm
from .models import Contract
from ..ads.models import Ads
from ..leads.models import Lead
from ..products.models import Product


class ContractListView(PermissionRequiredMixin, ListView):
    """Класс для отображения списка контрактов."""

    permission_required = "contracts.view_contract"
    model = Contract
    template_name = 'contracts/contracts-list.html'
    context_object_name = 'contracts'


class ContractDetailView(PermissionRequiredMixin, DetailView):
    """Класс для детального отображения контракта."""

    permission_required = "contracts.view_contract"
    model = Contract
    template_name = 'contracts/contracts-detail.html'


class ContractCreateView(PermissionRequiredMixin, View):
    """Класс для создания контракта."""

    permission_required = "contracts.add_contract"
    template_name = 'contracts/contracts-create.html'
    success_url = reverse_lazy('crm.contracts:contracts_list')

    def get(self, request):
        """
        Метод get проверяет есть ли в кэше параметр lead_id:
        если есть, то выдает форму с предзаполнеными данными,
        иначе выдает пустую.
        """
        lead_id = cache.get('lead_id')
        cache.delete('lead_id')
        if lead_id:
            lead = Lead.objects.filter(id=lead_id).first()
            ads = Ads.objects.filter(lead__id=lead_id).first()
            product = Product.objects.filter(ads__lead__id=lead_id).first()
            form = ContractForm(data={'lead': lead, 'ads': ads, 'product': product})
        else:
            form = ContractForm()

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Метод post сохраняет форму при ее валидности иначе возвращает форму с ошибками."""
        form = ContractForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form})


class ContractUpdateView(PermissionRequiredMixin, UpdateView):
    """Класс для обновления данных потенциального клиента."""

    permission_required = "contracts.change_contract"
    model = Contract
    template_name = 'contracts/contracts-edit.html'
    fields = '__all__'
    success_url = reverse_lazy('crm.contracts:contracts_list')


class ContractDeleteView(PermissionRequiredMixin, DeleteView):
    """Класс для удаления потенциального клиента."""

    permission_required = "contracts.delete_contract"
    model = Contract
    template_name = 'contracts/contracts-delete.html'
    success_url = reverse_lazy('crm.contracts:contracts_list')
