from django.shortcuts import render
from django.db.models.aggregates import Count, Min, Max, Avg, Sum
from store.models import Product,Customer, Order, OrderItem, Collection

def say_hello(request):
    orders = Order.objects.filter(customer__id=1).aggregate(Count('id'))
    units_sold = OrderItem.objects.filter(product__id=1).aggregate(total_units_sold=Sum('quantity'))
    calculate = Product.objects.filter(collection__id=3).aggregate(min_price=Min('unit_price'), max_price=Max('unit_price'), avg_price=Avg('unit_price'))

    return render(request, 'hello.html', {'name': 'Prathik', 'result': calculate})


