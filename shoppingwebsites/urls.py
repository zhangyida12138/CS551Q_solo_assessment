from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.Home, name='Home'),
    path('Home/', views.Home, name='Home1'),
    path('Cart/', views.Cart, name='Cart'),
    path('Cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('Cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('Purchase/',views.Purchase, name='Purchase'),
    path('search/',views.search,name='search'),
    path('orders/<int:order_id>/', views.Order_details, name='Order_details'),
    path('orders/', views.orders, name='orders'),
    path('Products/', views.products, name='products'),
    path('Products_detail/<int:product_id>/', views.Products_detail, name='Products_detail'),
    path('Profile/', views.Profile, name='Profile'),
    path('Login/', views.Login, name='Login'),
    path('Logout/', views.Logout, name='Logout'),
    path('Register/', views.Register, name='Register'),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)