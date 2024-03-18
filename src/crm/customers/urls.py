from django.urls import path

from .views import (CustomerListView,
                    CustomerCreateView,
                    CustomerDetailView,
                    CustomerUpdateView,
                    CustomerDeleteView)

app_name = 'crm.customers'

urlpatterns = [
    path('new/', CustomerCreateView.as_view(), name='customers_create'),
    path('<int:pk>/', CustomerDetailView.as_view(), name='customers_detail'),
    path('<int:pk>/edit/', CustomerUpdateView.as_view(), name='customers_edit'),
    path('<int:pk>/delete/', CustomerDeleteView.as_view(), name='customers_delete'),
    path('', CustomerListView.as_view(), name='customers_list'),
]
