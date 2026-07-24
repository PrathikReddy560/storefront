from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models
# Register your models here.

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
  search_fields = ['title']
  list_display = ['title','product_count']
  list_per_page = 10
  list_select_related = ['featured_product']

  @admin.display(ordering='products_count')
  def product_count(self, collection):
    url = (reverse('admin:store_product_changelist') 
           + '?'
           + urlencode({
             'collection__id': str(collection.id)
           }))
    return format_html('<a href="{}">{}</a>', url, collection.products_count)

  def get_queryset(self, request):
    return super().get_queryset(request).annotate(
      products_count=Count('products')
    )

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
  autocomplete_fields = ['collection']
  prepopulated_fields = {'slug': ['title']}
  actions = ['clear_inventory']
  list_display = ['title','unit_price','inventory_status','collection_title']
  list_editable = ['unit_price']
  list_filter = ['collection','last_update']
  list_per_page = 10
  list_select_related = ['collection']

  def collection_title(self,product):
    return product.collection.title

  @admin.display(ordering='inventory')
  def inventory_status(self,product):
    if product.inventory < 10:
      return 'LOW'
    return 'OK'

  def clear_inventory(self,request,queryset):
    updated_count = queryset.update(inventory=0)
    self.message_user(
      request,
      f'{updated_count} products were successfully updated.'
    )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
  list_display = ['first_name','last_name','membership','orders_count']
  list_editable = ['membership']
  ordering = ['first_name','last_name']
  list_per_page = 10
  search_fields = ['first_name__istartswith','last_name__istartswith'] 

  @admin.display(ordering='orders_count')
  def orders_count(self, customer):
    url = (reverse('admin:store_order_changelist') 
           + '?'
           + urlencode({
             'customer__id': str(customer.id)
           }))
    return format_html('<a href="{}">{}</a>', url, customer.orders_count)

  def get_queryset(self, request):
    return super().get_queryset(request).annotate(
      orders_count=Count('order')
    )

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
  list_display = ['id','placed_at','customer',]
  list_per_page = 10
  list_select_related = ['customer']
  autocomplete_fields = ['customer']

  def customer(self,order):
    return f'{order.customer.first_name} {order.customer.last_name}'