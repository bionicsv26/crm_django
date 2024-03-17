from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    """Класс формы для создания или редактирования товара (услуги)."""

    class Meta:
        model = Product
        fields = '__all__'
