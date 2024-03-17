from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ..ads.models import Ads
from ..crm import settings
# from ..customers.models import Customer
from ..leads.models import Lead
from ..products.models import Product


class IndexView(LoginRequiredMixin, TemplateView):
    """Класс для отображения базовой страницы index."""

    template_name = 'users/index.html'
    login_url = settings.LOGIN_URL

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products_count"] = Product.objects.all().count()
        context["advertisements_count"] = Ads.objects.all().count()
        context["leads_count"] = Lead.objects.all().count()
        # context["customers_count"] = Customer.objects.all().count()
        return context
