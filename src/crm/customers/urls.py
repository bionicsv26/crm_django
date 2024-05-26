from django.urls import path

from .views import (CustomerListView,
                    CustomerCreateView,
                    CustomerDetailView,
                    CustomerUpdateView,
                    CustomerDeleteView)

app_name = 'crm.customers'

urlpatterns = [
    path('new/', CustomerCreateView.as_view(), name='customer_create'),
    path('<int:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
    path('<int:pk>/edit/', CustomerUpdateView.as_view(), name='customer_edit'),
    path('<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer_delete'),
    path('', CustomerListView.as_view(), name='customers_list'),
]
