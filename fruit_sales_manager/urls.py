from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('fruitapp/', include('fruit_app.urls')),
    path('sales/', include('sales.urls')),
    path('statistics/', include('statistics_info.urls')),
]