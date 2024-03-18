from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.cache import cache
from django.db.models import Count, Sum, FloatField
from django.db.models.functions import Cast
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, DetailView, DeleteView

from .forms import AdsForm
from .models import Ads
from ..products.models import Product


class AdsListView(PermissionRequiredMixin, ListView):
    """Класс для отображения списка рекламных компаний."""

    permission_required = "ads.view_ads"
    model = Ads
    template_name = 'ads/ads-list.html'
    context_object_name = 'ads'


class AdsDetailView(PermissionRequiredMixin, DetailView):
    """Класс для детального отображения рекламной компании."""

    permission_required = "ads.view_ads"
    model = Ads
    template_name = 'ads/ads-detail.html'


class AdsCreateView(PermissionRequiredMixin, View):
    """Класс для создания рекламной компании."""

    permission_required = "ads.add_ads"
    template_name = 'ads/ads-create.html'
    success_url = reverse_lazy('crm.ads:ads_list')

    def get(self, request):
        """
        Метод get проверяет есть ли в кэше параметр product_id:
        если есть, то выдает форму с предзаполнеными данными,
        иначе выдает пустую.
        """
        product_id = cache.get('product_id')
        cache.delete('product_id')
        if product_id:
            product = Product.objects.filter(id=product_id).first()
            form = AdsForm(data={'product': product})
        else:
            form = AdsForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Метод post сохраняет форму при ее валидности иначе возвращает форму с ошибками."""
        form = AdsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


class AdsUpdateView(PermissionRequiredMixin, UpdateView):
    """Класс для обновления данных рекламной компании."""

    permission_required = "ads.change_ads"
    model = Ads
    template_name = 'ads/ads-edit.html'
    fields = '__all__'
    success_url = reverse_lazy('crm.ads:ads_list')


class AdsDeleteView(PermissionRequiredMixin, DeleteView):
    """Класс для удаления рекламной компании."""

    permission_required = "ads.delete_ads"
    model = Ads
    template_name = 'ads/ads-delete.html'
    success_url = reverse_lazy('crm.ads:ads_list')


class AdsStatisticView(LoginRequiredMixin, ListView):
    """Класс для страницы статистики."""

    template_name = 'ads/ads-statistic.html'
    context_object_name = 'ads'
    queryset = (Ads.objects.values('name')
                .annotate(
                    leads_count=Count('lead', distinct=True),
                    customers_count=Count('customer', distinct=True),
                    ads_budget=Sum('budget', distinct=True),
                    ads_profit=Sum('customer__contract__cost', distinct=True))
                .annotate(profit=(Cast('ads_profit', FloatField())
                          / Cast('ads_budget', FloatField())
                          )))
