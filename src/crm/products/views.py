from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView

from .forms import ProductForm
from .models import Product


class ProductListView(PermissionRequiredMixin, ListView):
    """Класс для отображения списка товаров (услуг)."""

    permission_required = "products.view_product"
    model = Product
    template_name = 'products/products-list.html'
    context_object_name = 'products'


class ProductDetailView(PermissionRequiredMixin, DetailView):
    """Класс для детального отображения данного товара (услуги)."""

    permission_required = "products.view_product"
    model = Product
    template_name = 'products/products-detail.html'


class ProductCreateView(PermissionRequiredMixin, CreateView):
    """Класс для создания товара (услуги)."""

    permission_required = "products.add_product"
    form_class = ProductForm
    template_name = 'products/products-create.html'
    success_url = reverse_lazy('crm.products:products_list')


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    """Класс для обновления данных данного товара (услуги)."""

    permission_required = "products.change_product"
    model = Product
    template_name = 'products/products-edit.html'
    fields = '__all__'


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    """Класс для удаления данного товара (услуги)."""

    permission_required = "products.delete_product"
    model = Product
    template_name = 'products/products-delete.html'
    success_url = reverse_lazy('crm.products:products_list')


class ProductTransferToAdsView(PermissionRequiredMixin, View):
    """Класс для создания рекламной компании на основании услуги."""

    permission_required = "ads.add_ads"

    def get(self, request, *args, **kwargs):
        """Метод get сохраняет в кэш значение product_id и запускает создание рекламной компании"""
        cache.set('product_id', kwargs['pk'], timeout=5)
        return HttpResponseRedirect(reverse_lazy('crm.ads:ads_create'))
