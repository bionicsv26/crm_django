from django import forms

from ..products.models import Product


class MixinProductForm(forms.ModelForm):
    """Класс миксина формы, включающий услуги."""

    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        empty_label="Услуга не выбрана",
        label='Услуга'
    )
