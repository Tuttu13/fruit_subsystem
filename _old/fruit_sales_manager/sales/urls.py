from . import sale_views
from django.urls import path

urlpatterns = [
    # 果物販売情報
    path('sales', sale_views.SaleListView.as_view(), name='sales'),
    path('salecreate', sale_views.createsale, name='salecreate'),
    path('saleupdate/<int:pk>', sale_views.editsale, name='saleupdate'),
    path('saledelete/<int:pk>', sale_views.SaleDeleteView.as_view(), name='saledelete'),
    path('import/', sale_views.csvimport, name='import'),
]