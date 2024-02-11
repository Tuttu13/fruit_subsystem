from django.urls import path

from . import fruit_views, views

urlpatterns = [
    # トップ画面
    path('', views.IndexView.as_view(), name='index'),
    # 果物マスタ
    path('list', fruit_views.FruitListView.as_view(), name='list'),
    # path('create', fruit_views.FruitCreateView.as_view(), name='create'),
    path('create', fruit_views.createfruit, name='create'),
    path('update/<int:pk>', fruit_views.editsale, name='update'),
    path('delete/<int:pk>', fruit_views.FruitDeleteView.as_view(), name='delete'),
]