from django import forms

from .models import Ads
from ..products.models import Product


class AdsForm(forms.ModelForm):
    """Класс формы для создания или редактирования рекламной компании."""

    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        empty_label="Услуга не выбрана",
        label='Услуга'
    )

    class Meta:
        model = Ads
        fields = '__all__'
