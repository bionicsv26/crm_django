from django.urls import path

from .views import (LeadListView,
                    LeadCreateView,
                    LeadDetailView,
                    LeadUpdateView,
                    LeadDeleteView,
                    LeadTransferToActiveView,
                    LeadTransferToContractView)

app_name = 'crm.leads'

urlpatterns = [
    path('new/', LeadCreateView.as_view(), name='leads_create'),
    path('<int:pk>/', LeadDetailView.as_view(), name='leads_detail'),
    path('<int:pk>/edit/', LeadUpdateView.as_view(), name='leads_edit'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='leads_delete'),
    path('<int:pk>/to_active/', LeadTransferToActiveView.as_view(), name='leads_to_active'),
    path('<int:pk>/to_contract/', LeadTransferToContractView.as_view(), name='leads_to_contract'),
    path('', LeadListView.as_view(), name='leads_list'),
]
