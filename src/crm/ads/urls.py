from django.urls import path

from .views import (AdsListView,
                    AdsCreateView,
                    AdsDetailView,
                    AdsUpdateView,
                    AdsDeleteView,
                    AdsStatisticView)

app_name = 'crm.ads'

urlpatterns = [
    path('new/', AdsCreateView.as_view(), name='ads_create'),
    path('<int:pk>/', AdsDetailView.as_view(), name='ads_detail'),
    path('<int:pk>/edit/', AdsUpdateView.as_view(), name='ads_edit'),
    path('<int:pk>/delete/', AdsDeleteView.as_view(), name='ads_delete'),
    path('statistic/', AdsStatisticView.as_view(), name='ads_statistic'),
    path('', AdsListView.as_view(), name='ads_list'),
]
