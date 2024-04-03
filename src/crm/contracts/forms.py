from django import forms
from django.core.exceptions import ValidationError

from .mixins import MixinLeadAdsForm
from .models import Contract
from ..ads.mixins import MixinProductForm


class ContractForm(MixinProductForm, MixinLeadAdsForm):
    """Класс формы для создания или редактирования контракта."""

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

    def clean_product(self):
        """Метод проверяет соответствует ли выбранная услуга выбранной компании"""
        ads = self.cleaned_data['ads']
        product = self.cleaned_data['product']
        if product.id != ads.product.id:
            self.add_error('product', 'Выбранная услуга не соответствует выбранной рекламной компании')
        return product
