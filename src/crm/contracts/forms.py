from django import forms
from django.core.exceptions import ValidationError

from .models import Contract
from ..ads.models import Ads
from ..leads.models import Lead
from ..products.models import Product


class ContractForm(forms.ModelForm):
    """Класс формы для создания или редактирования контракта."""

    lead = forms.ModelChoiceField(
        queryset=Lead.objects.filter(to_active=False),
        empty_label="Клиент не выбран",
        label='Потенциальный клиент'
    )
    ads = forms.ModelChoiceField(
        queryset=Ads.objects.all(),
        empty_label="Рекламная компания не выбрана",
        label='Рекламная компания')
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        empty_label="Услуга не выбрана",
        label='Услуга'
    )

    class Meta:
        model = Contract
        fields = '__all__'

    conclusion_day = forms.DateField(
        label='Дата заключения контракта',
        required=True,
        widget=forms.SelectDateWidget(attrs={'type': 'date'}),
        error_messages={'required': '', },
    )
    start_day = forms.DateField(
        label='Начало действия контракта',
        required=True,
        widget=forms.SelectDateWidget(attrs={'type': 'date'}),
        error_messages={'required': '', },
    )
    end_day = forms.DateField(
        label='Окончание действия контракта',
        required=True,
        widget=forms.SelectDateWidget(attrs={'type': 'date'}),
        error_messages={'required': '', },
    )

    def clean_end_day(self):
        """Метод проверяет соответствие даты конца договора дате начала договора."""
        start_day = self.cleaned_data['start_day']
        end_day = self.cleaned_data['end_day']
        if end_day < start_day:
            raise ValidationError('Дата окончания договора не может быть раньше даты его начала')

        return end_day

    def clean_ads(self):
        ads = self.cleaned_data['ads']
        lead = self.cleaned_data['lead']
        if lead.ads.id != ads.id:
            self.add_error('ads', 'Выбранная рекламная компания не соответствует'
                                  ' выбранному пользователю')
        return ads

    def clean_product(self):
        ads = self.cleaned_data['ads']
        product = self.cleaned_data['product']
        if product.id != ads.product.id:
            self.add_error('product', 'Выбранная услуга не соответствует выбранной рекламной акции')
        return product
