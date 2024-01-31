from . import views, fruit_views, sale_views
from django.urls import path

urlpatterns = [
    # TOP
    path('', views.IndexView.as_view(), name='index'),
    # 果物マスタ
    path('list', fruit_views.FruitListView.as_view(), name='list'),
    path('create', fruit_views.FruitCreateView.as_view(), name='create'),
    path('update/<int:pk>', fruit_views.FruitUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', fruit_views.FruitDeleteView.as_view(), name='delete'),
    # 果物販売情報
    path('sales', sale_views.SaleListView.as_view(), name='sales'),
    path('salecreate', sale_views.createsale, name='salecreate'),
    path('saleupdate/<int:pk>', sale_views.editsale, name='saleupdate'),
    path('saledelete/<int:pk>', sale_views.SaleDeleteView.as_view(), name='saledelete'),
    path('import/', views.csvimport, name='import'),
    # 販売統計情報
    path('statistics', sale_views.SaleListView.as_view(), name='statistics'),
]