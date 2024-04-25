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
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction

# Create your views here.
def Home(request):
    product_count=Products.objects.count()
    random_indexes=random.sample(range(product_count),32)#generate 32 random indexes
    products = [Products.objects.all()[index]for index in random_indexes]#get 30 randoms products
    return render(request,'Home.html',{'Products':products})

def search(request):
    query = request.GET.get('query','')
    if query:
        results = Products.objects.filter(product_name__icontains=query)
    else:
        results = Products.objects.none()
    
    return render(request,'search.html',{'results':results})

def Products_detail(request,product_id):

    product = get_object_or_404(Products,pk=product_id)

    return render(request,'Products_detail.html',{'product':product})

def products(request):
    categories = Products.objects.values_list('category', flat=True).distinct()
    products = Products.objects.all()
    category = request.GET.get('category')

    if category:
        products = products.filter(category=category)

    return render(request, 'Products.html', {
        'categories': categories,
        'Products': products,
        'selected_category': category
    })

@login_required
def Cart(request):
    cart_items = Shopping_Cart.objects.filter(user=request.user).select_related('product')
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'Cart.html', {'cart_items': cart_items,'total_price':total_price})

@login_required
def update_cart(request,product_id):
    product = get_object_or_404(Products, pk=product_id)
    cart_item = Shopping_Cart.objects.get(user=request.user, product=product)
    action = request.POST.get('action')
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        cart_item.quantity -= 1
        if cart_item.quantity < 1:
            cart_item.quantity = 1  # at least have one 
    cart_item.save()
    return redirect('Cart')

@login_required
def remove_from_cart(request, product_id):
    Shopping_Cart.objects.filter(user=request.user, product_id=product_id).delete()
    return HttpResponseRedirect(reverse('Cart'))

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
     # Make sure to get the quantity. If it is a form submission, get it from the form data.
    quantity = int(request.POST.get('quantity', 1))

     # get_or_create will try to get an existing entry, or create a new one
    cart_item, created = Shopping_Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': quantity} # Provide default values to use when creating new entries
    )
    if not created:
         # If the entry already exists, increase the number and save it
        cart_item.quantity += quantity
        cart_item.save()

    return redirect('Cart') # Redirect to the shopping cart details page


@login_required
def orders(request):
    order_list = Orders.objects.filter(user=request.user).order_by('-order_date') 
    return render(request, 'Orders.html', {'order_list': order_list})

@login_required
def Order_details(request,order_id):
    try:
        order = Orders.objects.get(id=order_id, user=request.user)
    except Orders.DoesNotExist:
        return render(request, 'error.html', {'error': 'Order not found or access denied.'})
    order_details = order.order_details_set.all() 
    return render(request, 'Order_details.html', {
        'order': order,
        'order_details': order_details
    })

@login_required
def Profile(request):
    return render(request,'Profile.html',{'user':request.user})

@login_required
def Purchase(request):
    with transaction.atomic():
        cart_items = Shopping_Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return redirect('Cart')

        total_price = sum(item.product.price * item.quantity for item in cart_items)
        new_order = Orders.objects.create(
            user=request.user,
            order_date=timezone.now(),
            total_price=total_price,
            order_status='to_be_paid'
        )

        for item in cart_items:
            Order_Details.objects.create(
                order=new_order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart_items.delete()
    return redirect('orders')

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