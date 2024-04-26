"""
URL configuration for shopping project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from shoppingwebsites import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/',views.admin,name='admin'),
    path('admin/admin_delete_products/<int:product_id>/',views.admin_delete_products,name='admin_delete_products'),
    path('admin/admin_Order_details/<int:order_id>/',views.admin_Order_details,name='admin_Order_details'),
    path('admin/order_delete/<int:order_id>/',views.order_delete,name='order_delete'),
    path('admin/admin_chart',views.admin_chart,name='admin_chart'),
    path('admin/database',views.admin_database,name='admin_database'),
    path('admin/customer_list',views.customer_list,name='customer_list'),
    path('admin/customer_delete/<int:customer_id>/',views.customer_delete,name='customer_delete'),
    path('admin/customer_edit/<int:customer_id>/',views.customer_edit,name='customer_edit'),
    path('', include('shoppingwebsites.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

