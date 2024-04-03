from .mixins import MixinProductForm
from .models import Ads


class AdsForm(MixinProductForm):
    """Класс формы для создания или редактирования рекламной компании."""

    class Meta:
        model = Ads
        fields = '__all__'
