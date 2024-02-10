from django.urls import path

from . import views

urlpatterns = [
    path('', views.loginfunc, name='login'),
    path('login/', views.loginfunc, name='login'),
    path('signup/', views.signupfunc, name='signup'),
]