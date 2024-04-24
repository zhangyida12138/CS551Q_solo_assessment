from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from django.db.models import Prefetch
from urllib.parse import quote
from django.core.exceptions import FieldError
from shoppingwebsites.models import Users,Products,Orders,Order_Details,Shopping_Cart
from django.shortcuts import render, get_object_or_404, redirect
import random
from django.contrib.auth import login
from .forms import CustomUserCreationForm

# Create your views here.
def Home(request):
    product_count=Products.objects.count()
    random_indexes=random.sample(range(product_count),32)#generate 32 random indexes
    products = [Products.objects.all()[index]for index in random_indexes]#get 30 randoms products
    return render(request,'Home.html',{'Products':products})

def Products_detail(request):
    pass

def products(request):
    return render(request,'Products.html')

def Cart(request):
    return render(request,'Products.html')

def Orders(request):
    return render(request,'Products.html')

def Order_details(request):
    return render(request,'Products.html')

def Profile(request):
    return render(request,'Products.html')

def Purchase(request):
    return render(request,'Products.html')

def Login(request):
    return render(request,'registration/Login.html')

def Logout(request):
    return render(request,'Products.html')

def Register(request):
    if request.method =='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user= form.save()
            login(request, user)#login as new user
            print('successfully Register!')
            return redirect('Home')
    else:
        form =CustomUserCreationForm()
    return render(request,'registration/Register.html',{'form':form})