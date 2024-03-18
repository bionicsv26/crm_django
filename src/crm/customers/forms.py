from django import forms

from .models import Customer
from ..ads.models import Ads
from ..contracts.models import Contract
from ..leads.models import Lead


class CustomerForm(forms.ModelForm):
    """Класс формы для создания или редактирования покупателя."""

    lead = forms.ModelChoiceField(
        queryset=Lead.objects.filter(to_active=False),
        empty_label="Клиент не выбран",
        label='Потенциальный клиент'
    )
    ads = forms.ModelChoiceField(
        queryset=Ads.objects.all(),
        empty_label="Рекламная компания не выбрана",
        label='Рекламная компания')
    contract = forms.ModelChoiceField(
        queryset=Contract.objects.all(),
        empty_label="Контракт не выбран",
        required=False,
        label='Контракт'
    )

    class Meta:
        model = Customer
        fields = '__all__'

    def clean_ads(self):
        ads = self.cleaned_data['ads']
        lead = self.cleaned_data['lead']
        if lead.ads.id != ads.id:
            self.add_error('ads', 'Выбранная рекламная компания не соответствует'
                                  ' выбранному пользователю')
        return ads

    def clean_contract(self):
        ads = self.cleaned_data['ads']
        lead = self.cleaned_data['lead']
        contract = self.cleaned_data['contract']
        if contract is not None:
            if lead.id != contract.lead.id:
                self.add_error('contract', 'Выбранный контракт не соответствует'
                                           ' выбранному пользователю')
            if ads.id != contract.ads.id:
                self.add_error('contract', 'Выбранный контракт не соответствует'
                                           ' выбранноq рекламной компании')
        return contract
