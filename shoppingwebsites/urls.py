from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('Home/', views.Home, name='Home1'),
    path('Cart/', views.Cart, name='Cart'),
    path('Order_details/', views.Order_details, name='Order_details'),
    path('Orders/', views.Orders, name='Orders'),
    path('Products/', views.products, name='products'),
    path('Products_detail/', views.Products_detail, name='Products_detail'),
    path('Profile/', views.Profile, name='Profile'),
    path('Login/', auth_views.LoginView.as_view(template_name='registration/Login.html'), name='Login'),
    path('Logout/', auth_views.LogoutView.as_view(), name='Logout'),
    path('Register/', views.Register, name='Register'),
]