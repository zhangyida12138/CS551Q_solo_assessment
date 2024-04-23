from django.db import models

class Users(models.Model):
    username=models.CharField(max_length=50,db_index=True)#add a index here
    password=models.CharField(max_length=255)
    email=models.EmailField(max_length=100,db_index=True)
    phone=models.CharField(max_length=20)
    address=models.CharField(max_length=255)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

class Products(models.Model):
    product_name=models.CharField(max_length=100)
    description=models.TextField()
    product_url=models.URLField(max_length=200, blank=True)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    discount_price=models.DecimalField(max_digits=10, decimal_places=2)
    stock=models.PositiveIntegerField()
    category=models.CharField(max_length=50)
    rating=models.DecimalField(max_digits=5, decimal_places=1, default=5.0)
    no_of_ratings=models.PositiveIntegerField()
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    class Meta:
        indexes=[
            models.Index(fields=['product_name']),
            models.Index(fields=['price']),
            models.Index(fields=['category']),
            models.Index(fields=['category','price'])
        ]#index here

class Orders(models.Model):
    order_date=models.DateTimeField()
    total_price=models.DecimalField(max_digits=10,decimal_places=2)
    order_status=models.CharField(
        max_length=50,
        choices=[('to_be_paid','to_be_paid'),
        ('paid','paid'),
        ('shipped','shipped'),
        ('cancelled','cancelled')])
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    class Meta:
        indexes=[
            models.Index(fields=['order_date']),
            models.Index(fields=['order_status']),
            models.Index(fields=['order_date','order_status'])
        ]#index here

class Order_Details(models.Model):
    order_id=models.ForeignKey(Orders, on_delete=models.CASCADE)
    product_id=models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

class Shopping_Cart(models.Model):
    user_id=models.ForeignKey(Users, on_delete=models.CASCADE)
    product_id=models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

# Create your models here.
