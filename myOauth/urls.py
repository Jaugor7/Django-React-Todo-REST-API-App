from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'myOauth'

urlpatterns = [
 
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('logoutPage/', views.logoutPage, name="logoutPage"),
    path('register/', views.register, name="register"),
    path('not_found/', views.not_found,name="not_found" ),
    path('activate/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activate'),
]
