from . import views, fruit_views
from django.urls import path

urlpatterns = [
    # TOP
    path('', views.IndexView.as_view(), name='index'),
    # 果物マスタ
    path('list', fruit_views.FruitListView.as_view(), name='list'),
    path('create', fruit_views.FruitCreateView.as_view(), name='create'),
    path('update/<int:pk>', fruit_views.FruitUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', fruit_views.FruitDeleteView.as_view(), name='delete'),
]