from django.urls import path
from django.contrib import admin
from .import views



urlpatterns= [
    path('accounts/login/', views.login_view, name="login_page"),
    path('accounts/logout/', views.logout_view, name="logout_page"),
    path('accounts/signup/', views.signup_view, name="signup_page"),
    path('accounts/contact/', views.contact_view, name="contact_page"),
    path('', views.home, name="home_page"),
]