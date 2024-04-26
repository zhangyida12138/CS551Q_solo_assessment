from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from django.db.models import Prefetch,Count, Case, When, Value, CharField,Sum, F
from urllib.parse import quote
from django.core.exceptions import FieldError
from shoppingwebsites.models import Users,Products,Orders,Order_Details,Shopping_Cart
from django.shortcuts import render, get_object_or_404, redirect
import random
from django.contrib.auth import login,authenticate,logout,update_session_auth_hash
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.utils import timezone
from django.db import transaction
from django.contrib import messages
from django.db.models.functions import TruncDay
from django.http import JsonResponse
import json

# Create your views here.
# Home page view: Displays a random selection of 100 products.
def Home(request):
    try:
        product_count=Products.objects.count()
        random_indexes=random.sample(range(product_count),100)#generate 100 random indexes
        products = [Products.objects.all()[index]for index in random_indexes]#get 30 randoms products
        return render(request,'Home.html',{'Products':products})
    except Exception as e:
        return render(request,'error.html',{'error':str(e)})

# Search functionality: Filters products based on the 'query' parameter from GET request.
def search(request):
    try:
        query = request.GET.get('query','')
        if query:
            results = Products.objects.filter(product_name__icontains=query)
        else:
            results = Products.objects.none()
        
        return render(request,'search.html',{'results':results})
    except Exception as e:
        return render(request,'error.html',{'error':str(e)})


# Product details view: Displays details for a specific product identified by 'product_id'.
def Products_detail(request,product_id):
    try:
        product = get_object_or_404(Products,pk=product_id)
        return render(request,'Products_detail.html',{'product':product})
    except Http404 as e:
        return render(request,'error.html',{'error':str(e)})
    except Exception as e:
        return render(request,'error.html',{'error':str(e)})

# Products view: Lists all products or filters by category if 'category' parameter is provided.
def products(request):
    try:
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
    except Exception as e:
        return render(request,'error.html',{'error':str(e)})

# Cart view: Manages and displays the shopping cart for logged-in users or through session for guests.
def Cart(request):
    try:
        if request.user.is_authenticated:
            cart_items = Shopping_Cart.objects.filter(user=request.user).select_related('product')
            total_price = sum(item.product.discount_price * item.quantity for item in cart_items)
        else:
            cart = request.session.get('cart', {})
            cart_items = []
            total_price = 0
            for pid, details in cart.items():
                product = Products.objects.get(pk=pid)
                quantity = details['quantity']
                total_price += product.discount_price * quantity
                cart_items.append({'product': product, 'quantity': quantity})

        return render(request, 'Cart.html', {'cart_items': cart_items, 'total_price': total_price})
    except Exception as e:
        return render(request,'error.html',{'error':str(e)})

# Updates the quantity of a specific product in the cart, for either logged-in users or session-stored carts.
def update_cart(request, product_id):
    try:
        product = get_object_or_404(Products, pk=product_id)
        action = request.POST.get('action')
        quantity_change = 1 if action == 'increase' else -1

        if request.user.is_authenticated:
            cart_item, created = Shopping_Cart.objects.get_or_create(user=request.user, product=product)
            cart_item.quantity = max(1, cart_item.quantity + quantity_change)
            cart_item.save()
        else:
            cart = request.session.get('cart', {})
            if str(product_id) in cart:
                # Ensure that the quantity is updated while handling the case where the item already exists in the shopping cart
                cart[str(product_id)]['quantity'] = max(1, cart[str(product_id)]['quantity'] + quantity_change)
            else:
                #Initialize the quantity of items in the shopping cart
                cart[str(product_id)] = {'quantity': 1}
            request.session['cart'] = cart
            request.session.modified = True # Explicitly mark the session as modified to ensure changes are saved

        return redirect('Cart')        
    except Http404 as e:
        return render(request,'error.html',{'error':str(e)})
    except Exception as e:
        return render(request,'error.html',{'error':str(e)})

# Removes a specific product from the cart.
def remove_from_cart(request, product_id):
    try:
        if request.user.is_authenticated:
            Shopping_Cart.objects.filter(user=request.user, product_id=product_id).delete()
        else:
            cart = request.session.get('cart', {})
            if product_id in cart:
                del cart[product_id]
                request.session['cart'] = cart
        return redirect('Cart')
    except Exception as e:
        return render(request,'error.html',{'error':str(e)})

# Adds a product to the cart, handling both logged-in and guest users.
def add_to_cart(request, product_id):
    try:
        product = get_object_or_404(Products, pk=product_id)
        quantity = int(request.POST.get('quantity', 1)) # Try to get the quantity, if not provided, the default is 1

        if request.user.is_authenticated:
            # Login user: directly operate the database
            cart_item, created = Shopping_Cart.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': 0} # Note: If it is a newly created entry, initialize it to 0 first
            )
            cart_item.quantity += quantity # Existing or newly created items, plus the newly added quantity
            cart_item.save()
        else:
            # Not logged in users: use sessions to store shopping cart data
            cart = request.session.get('cart', {})
            product_id_str = str(product_id) # Use the product ID in string form to avoid JSON serialization issues
            if product_id_str in cart:
                cart[product_id_str]['quantity'] += quantity
            else:
                cart[product_id_str] = {'quantity': quantity, 'price': str(product.price)}
            request.session['cart'] = cart
            request.session.modified = True # Explicitly mark the session as modified to ensure changes are saved

        return redirect('Cart')
    except Http404 as e:
        return render(request,'error.html',{'error':str(e)})
    except Exception as e:
        return render(request,'error.html',{'error':str(e)})

# check all the orders
@login_required
def orders(request):
    try:
        order_list = Orders.objects.filter(user=request.user).order_by('-order_date') 
        return render(request, 'Orders.html', {'order_list': order_list})
    except Http404 as e:
        return render(request,'error.html',{'error':str(e)})
    except Exception as e:
        return render(request,'error.html',{'error':str(e)})

# check orderdetail page
@login_required
def Order_details(request,order_id):
    try:
        order = Orders.objects.get(id=order_id, user=request.user)
    except Orders.DoesNotExist:
        return render(request, 'error.html', {'error': 'Order not found or access denied.'})
    try:
        order_details = order.order_details_set.all() 
        return render(request, 'Order_details.html', {
            'order': order,
            'order_details': order_details
        })
    except Exception as e:
        return render(request,'error.html',{'error':str(e)})

# load profile page
@login_required
def Profile(request):
    try:
        return render(request,'Profile.html',{'user':request.user})
    except Exception as e:
        return render(request,'error.html',{'error':str(e)})

# Processes and completes the purchase, creates an order, clears the cart, and sends a success message.
def Purchase(request):
    try:
        if request.user.is_authenticated:
            cart_items_query = Shopping_Cart.objects.filter(user=request.user)
            # Convert QuerySet to list of dicts to standardize processing later on
            cart_items = [{'product': item.product, 'quantity': item.quantity} for item in cart_items_query]
        else:
            cart_items = []
            cart = request.session.get('cart', {})
            for pid, details in cart.items():
                product = Products.objects.get(pk=pid)
                cart_items.append({'product': product, 'quantity': details['quantity']})
        
        if not cart_items:
            return redirect('Cart')

        total_price = sum(item['product'].discount_price * item['quantity'] for item in cart_items)
        new_order = Orders.objects.create(
            user=request.user if request.user.is_authenticated else None,
            order_date=timezone.now(),
            total_price=total_price,
            order_status='to_be_paid'
        )

        for item in cart_items:
            Order_Details.objects.create(
                order=new_order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )

        if request.user.is_authenticated:
            Shopping_Cart.objects.filter(user=request.user).delete()
        else:
            del request.session['cart']  
        messages.add_message(request, messages.SUCCESS, 'Purchase completed successfully!')
        return redirect('Home')
    except Http404 as e:
        return render(request,'error.html',{'error':str(e)})
    except Exception as e:
        return render(request,'error.html',{'error':str(e)})

# different account log in the different page.
def Login(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                print('successfully login!')
                login(request, user)
                if user.is_superuser or user.is_staff:
                    print('successfully login admin!')
                    return redirect('admin')
                else:
                    print('successfully login user!')
                    return redirect('Home')
            else:
                messages.error(request, 'Invalid email or password.')
        return render(request, 'registration/Login.html')
    except Exception as e:
        return render(request,'error.html',{'error':str(e)})


def Logout(request):
    try:
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Logout successfully!')
        return redirect('Home')
    except Exception as e:
        return render(request,'error.html',{'error':str(e)})

# use email as account
def Register(request):
    try:
        if request.method =='POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user= form.save()
                login(request, user)#login as new user
                print('successfully Register!')
                messages.add_message(request, messages.SUCCESS, 'Register successfully!')
                return redirect('Home')
        else:
            form =CustomUserCreationForm()
        return render(request,'registration/Register.html',{'form':form})
    except Exception as e:
        return render(request,'error.html',{'error':str(e)})    

# admin dashboard page
@login_required
@user_passes_test(lambda u: u.is_staff)
def admin(request):
    try:
        orders = Orders.objects.all().order_by('-order_date')
        return render(request, 'admin/admin.html', {'orders': orders})
    except Exception as e:
        return render(request,'error.html',{'error':str(e)})

# check all the orders include guest and customer
@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_Order_details(request,order_id):
    try:
        order = Orders.objects.get(id=order_id)
    except Orders.DoesNotExist:
        return render(request, 'error.html', {'error': 'Order not found or access denied.'})
    try:
        order_details = order.order_details_set.all() 
        return render(request, 'admin/admin_Order_details.html', {
            'order': order,
            'order_details': order_details
        })
    except Exception as e:
        return render(request,'error.html',{'error':str(e)})

# delete orders
@login_required
@user_passes_test(lambda u: u.is_staff)
def order_delete(request,order_id):
    try:
        if request.method == 'POST':
            order = get_object_or_404(Orders, id=order_id)
            order.delete()
            messages.success(request, "Order deleted successfully.")
            return redirect('admin')
        else:
            messages.error(request, "Invalid request")
            return redirect('admin')
    except Http404 as e:
        return render(request,'error.html',{'error':str(e)})
    except Exception as e:
        return render(request,'error.html',{'error':str(e)})

# view all the products
@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_database(request):
    try:
        categories = Products.objects.values_list('category', flat=True).distinct()
        products = Products.objects.all()
        category = request.GET.get('category')

        if category:
            products = products.filter(category=category)

        return render(request, 'admin/admin_database.html', {
            'categories': categories,
            'Products': products,
            'selected_category': category
        })
    except Exception as e:
        return render(request,'error.html',{'error':str(e)})

# delete products
@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_delete_products(request,product_id):
    try:
        product=get_object_or_404(Products, id=product_id)
        product.delete()
        messages.success(request, "Products deleted successfully.")
        return redirect('admin_database')
    except Http404 as e:
        return render(request,'error.html',{'error':str(e)})
    except Exception as e:
        return render(request,'error.html',{'error':str(e)})

# delete user include staff and superuser and customer
@login_required
@user_passes_test(lambda u: u.is_superuser)
@permission_required('auth.delete_user')
def customer_delete(request,customer_id):
    try:
        if request.method == 'POST':
            customer = get_object_or_404(Users, id=customer_id)
            customer.delete()
            messages.success(request, "Customer deleted successfully.")
            return redirect('customer_list')
        else:
            messages.error(request, "Invalid request")
            return redirect('customer_list')
    except Http404 as e:
        return render(request,'error.html',{'error':str(e)})
    except Exception as e:
        return render(request,'error.html',{'error':str(e)})

# change password
@login_required
@user_passes_test(lambda u: u.is_superuser)
@permission_required('auth.change_user')
def customer_edit(request, customer_id):
    try:
        user = get_object_or_404(Users, pk=customer_id)
        if request.method == 'POST':
            password = request.POST.get('password')
            if password:
                user.set_password(password)  
                user.save()  
                update_session_auth_hash(request, user)  
                messages.success(request, "Password updated successfully.")
            return redirect('customer_list')
        return render(request, 'admin/customer_edit.html', {'customer': user})
    except Http404 as e:
        return render(request,'error.html',{'error':str(e)})
    except Exception as e:
        return render(request,'error.html',{'error':str(e)})

# view all the accounts
@login_required
@user_passes_test(lambda u: u.is_staff)
@permission_required('auth.view_user', raise_exception=True)
def customer_list(request):
    try:
        customer_list=Users.objects.all()
        return render(request,'admin/customer_list.html',{'customer_list':customer_list})
    except Http404 as e:
        return render(request,'error.html',{'error':str(e)})
    except Exception as e:
        return render(request,'error.html',{'error':str(e)})

# check the sales conditions
@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_chart(request):
    try:
        # Data for purchase types (Logged In vs Guest)
        purchase_type_data = Orders.objects.annotate(
            purchase_type=Case(
                When(user__isnull=False, then=Value('Logged In')),
                default=Value('Guest'),
                output_field=CharField(),
            )
        ).values('purchase_type').annotate(total=Count('id')).order_by('purchase_type')

        # Data for sales by product category
        category_data = Order_Details.objects.values('product__category').annotate(
        total=Sum('quantity') 
        ).order_by('product__category')

        # Convert data to lists for Chart.js
        purchase_types = [x['purchase_type'] for x in purchase_type_data]
        purchase_totals = [x['total'] for x in purchase_type_data]
        categories = [x['product__category'] for x in category_data]
        category_totals = [x['total'] for x in category_data]

        # Data for sales over time line chart
        sales_over_time_data = Order_Details.objects \
            .annotate(date=TruncDay('order__order_date')) \
            .values('date', 'product__product_name') \
            .annotate(total_sales=Sum('quantity')) \
            .order_by('date', 'product__product_name')

        # Reformat the sales data for the line chart
        line_chart_data = {}
        for item in sales_over_time_data:
            product_name = item['product__product_name']
            if product_name not in line_chart_data:
                line_chart_data[product_name] = {'dates': [], 'sales': []}
            line_chart_data[product_name]['dates'].append(item['date'].strftime('%Y-%m-%d'))
            line_chart_data[product_name]['sales'].append(item['total_sales'])

        context = {
            'purchase_types': purchase_types,
            'purchase_totals': purchase_totals,
            'categories': categories,
            'category_totals': category_totals,
            'line_chart_data': line_chart_data
        }
        return render(request, 'admin/admin_chart.html', context)
    except Http404 as e:
        return render(request,'error.html',{'error':str(e)})
    except Exception as e:
        return render(request,'error.html',{'error':str(e)})
        