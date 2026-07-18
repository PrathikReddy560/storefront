from django.db import models

# Create your models here.

class Promotion(models.Model):
  description = models.CharField(max_length=255)
  discount = models.FloatField()

class Collection(models.Model):
  title = models.CharField(max_length=100)
  featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')
 
#------------PRODUCTS-----------------
class Product(models.Model):
  MEMBERSHIP_BRONZE = 'B'
  MEMBERSHIP_SILVER = 'S'
  MEMBERSHIP_GOLD = 'G'
  MEMBERSHIP_CHOICES = [
    (MEMBERSHIP_BRONZE, 'Bronze'),
    (MEMBERSHIP_SILVER, 'Silver'),
    (MEMBERSHIP_GOLD, 'Gold'),
  ]
  title  = models.CharField(max_length=100)
  description = models.TextField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  inventory = models.IntegerField()
  last_update = models.DateTimeField(auto_now=True)
  membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
  collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
  promotions = models.ManyToManyField(Promotion, blank=True)

#------------ITEMS-----------------
class Item(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField()
  unit_price = models.DecimalField(max_digits=10, decimal_places=2)

#------------ORDERS-----------------
class Order(models.Model):
  PENDING = 'P'
  COMPLETE = 'C'
  FAILED = 'F'
  PAYMENT_STATUS_CHOICES = [
    (PENDING, 'Pending'),
    (COMPLETE, 'Complete'),
    (FAILED, 'Failed'),
  ]
  placed_at = models.DateTimeField(auto_now_add=True)
  payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PENDING)
  item = models.ManyToManyField(Item, related_name='orders')
  customer = models.OneToOneField('Customer', on_delete=models.PROTECT, related_name='orders')

#------------CUSTOMERS-----------------
class Customer(models.Model):
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  email = models.EmailField(unique=True)
  phone = models.CharField(max_length=20, blank=True, null=True)
  birth_date = models.DateField(blank=True, null=True)

#------------ORDERITEMS-----------------
class OrderItem(models.Model):
  order = models.ForeignKey(Order, on_delete=models.PROTECT)
  product = models.ForeignKey(Item, on_delete=models.PROTECT)
  quantity = models.PositiveIntegerField()
  unit_price = models.DecimalField(max_digits=10, decimal_places=2)

#------------ADDRESS-----------------
class Address(models.Model):
  street = models.CharField(max_length=255)
  city = models.CharField(max_length=100)
  zip_code = models.CharField(max_length=20)
  customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)

#------------CART-----------------
class Cart(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField()


