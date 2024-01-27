from django.contrib import admin
from django.urls import path, include
import account

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('fruitapp/', include('fruit_app.urls')),
]