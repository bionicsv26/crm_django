from django.urls import path

from .views import (ProductListView,
                    ProductCreateView,
                    ProductDetailView,
                    ProductUpdateView,
                    ProductDeleteView,
                    ProductTransferToAdsView)

app_name = 'crm.products'

urlpatterns = [
    path('new/', ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('<int:pk>/to_ads/', ProductTransferToAdsView.as_view(), name='product_to_ads'),
    path('', ProductListView.as_view(), name='products_list'),
]
