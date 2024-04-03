from django import forms

from ..ads.models import Ads
from ..leads.models import Lead


class MixinLeadAdsForm(forms.ModelForm):
    """Класс миксина формы, включающий рекламную компанию и потенциального клиента."""

    lead = forms.ModelChoiceField(
        queryset=Lead.objects.filter(to_active=False),
        empty_label="Клиент не выбран",
        label='Потенциальный клиент'
    )
    ads = forms.ModelChoiceField(
        queryset=Ads.objects.all(),
        empty_label="Рекламная компания не выбрана",
        label='Рекламная компания')

    def clean_ads(self):
        """Метод проверяет соответствует ли выбранная компания пользователю"""
        ads = self.cleaned_data['ads']
        lead = self.cleaned_data['lead']
        if lead.ads.id != ads.id:
            self.add_error('ads', 'Выбранная рекламная компания не соответствует'
                                  ' выбранному пользователю')
        return ads
