from . import views
from django.urls import path

urlpatterns = [
    # アカウント登録画面
    path('signup/', views.signup_view, name='signup'),
    # ログイン画面
    path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),
    path('user/', views.user_view, name='user'),
    path('other/', views.other_view, name='other'),
]