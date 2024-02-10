from . import statistics_views
from django.urls import path

urlpatterns = [
    # 販売統計情報
    path('', statistics_views.SaleListView.as_view(), name='statistics'),
]