from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from django.db.models import Prefetch
from urllib.parse import quote
from django.core.exceptions import FieldError
from shoppingwebsites.models import Users,Products,Orders,Order_Details,Shopping_Cart
from django.shortcuts import render, get_object_or_404
import random

# Create your views here.
def Home(request):
    product_count=Products.objects.count()
    random_indexes=random.sample(range(product_count),30)#generate 30 random indexes
    products = [Products.objects.all()[index]for index in random_indexes]#get 30 randoms products
    return render(request,'Home.html',{'Products':products})

def Products_detail(request):
    pass