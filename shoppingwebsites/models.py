from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Use email to log in
    REQUIRED_FIELDS = []  # Required when creating a superuser

    def __str__(self):
        return self.email

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
    user=models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
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
    order=models.ForeignKey(Orders, on_delete=models.CASCADE)
    product=models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

class Shopping_Cart(models.Model):
    user=models.ForeignKey(Users, on_delete=models.CASCADE)
    product=models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

# Create your models here.
