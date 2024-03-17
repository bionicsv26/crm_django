from django import forms

from .models import Lead


class LeadForm(forms.ModelForm):
    """Класс формы для создания или редактирования потенциального клиента."""

    class Meta:
        model = Lead
        fields = '__all__'

    phone = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '+7 (___) ___-__-__', 'id': 'phone'}),
        label='Телефон',
        required=True,
    )
