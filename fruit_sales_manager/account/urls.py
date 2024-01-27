from . import views
from django.urls import path

urlpatterns = [
    path('', views.loginfunc, name='login'),
    path('login/', views.loginfunc, name='login'),
    path('signup/', views.signupfunc, name='signup'),
    # path('other/', views.other_view, name='other'),
]