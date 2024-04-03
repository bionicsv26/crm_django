from django import forms

from .models import Customer
from ..contracts.mixins import MixinLeadAdsForm
from ..contracts.models import Contract


class CustomerForm(MixinLeadAdsForm):
    """Класс формы для создания или редактирования покупателя."""

    contract = forms.ModelChoiceField(
        queryset=Contract.objects.all(),
        empty_label="Контракт не выбран",
        required=False,
        label='Контракт'
    )

    class Meta:
        model = Customer
        fields = '__all__'

    def clean_contract(self):
        """Метод проверяет соответствует ли выбранный контракт пользователю и компании"""
        ads = self.cleaned_data['ads']
        lead = self.cleaned_data['lead']
        contract = self.cleaned_data['contract']
        if contract is not None:
            if lead.id != contract.lead.id:
                self.add_error('contract', 'Выбранный контракт не соответствует'
                                           ' выбранному пользователю')
            if ads.id != contract.ads.id:
                self.add_error('contract', 'Выбранный контракт не соответствует'
                                           ' выбранной рекламной компании')
        return contract
