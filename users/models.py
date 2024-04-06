from django.db import models
from django.contrib.auth.models import AbstractUser
# from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.conf import settings



# Create your models here.
class NewUser(AbstractUser):
    current_date = datetime.date.today()
    USER_TYPE_CHOICES = (('admin', 'admin'),
    ('customer', 'customer'),
    )
    GENDER_TYPE_CHOICES = (('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
    )
    user_type = models.CharField(max_length=300,choices=USER_TYPE_CHOICES,default='admin')
    profile_photo = models.ImageField(upload_to ='customer_images/')
    date_registered = models.DateField(default=timezone.now)
    gender = models.CharField(max_length=300,choices=GENDER_TYPE_CHOICES,default='Male')
    date_of_birth = models.DateField(null=True)
    city = models.CharField(max_length=300,default='Hubli')
    contact = models.CharField(max_length=300,default='9590499570')
    state = models.CharField(max_length=300,default='Karnataka')
    country = models.CharField(max_length=300,default='India')
    address = models.CharField(max_length=300)


class Category(models.Model):
    title = models.CharField(max_length=300,unique = True)
    status = models.CharField(max_length=300,default='active')

class Product(models.Model):
    title = models.CharField(max_length=300,unique = True)
    description = models.TextField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    sku = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    dimensions = models.CharField(max_length=255)
    availability = models.BooleanField(default=True)
    product_image = models.ImageField(upload_to='product_variants/')


class Cart(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    products = models.ManyToManyField('ProductForm', through='CartItem')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(default=timezone.now)
    

class CartItem(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('ProductForm', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1) 
    
    
class Checkout(models.Model):
    PAYMENT_CHOICES = (
        ('cash_on_delivery', 'Cash on Delivery'),
        ('online_payment', 'Online Payment'),)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=300)
    total_price = models.IntegerField(default='120')
    payment_option = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    cart = models.ForeignKey(Cart, related_name='checkout', on_delete=models.CASCADE,default=None)
    date_time = models.DateTimeField(default=timezone.now)
 
class onlinepayment(models.Model):
    amount = models.IntegerField()
    payment_id = models.CharField(max_length=255)
    paid = models.BooleanField(default=False)
    user_id=models.ForeignKey('NewUser',on_delete=models.CASCADE,default=0)

class ProductForm(models.Model):
    uname =models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    quantity = models.CharField(max_length=255)
    img = models.ImageField(upload_to='static\images')
    district = models.CharField(max_length=20, default='xyz')


class Farmer(models.Model):
    name = models.CharField(max_length=30)
    uname = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    district = models.CharField(max_length=20)
    phone = models.CharField(max_length=10)