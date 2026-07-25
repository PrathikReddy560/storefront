from django.shortcuts import get_object_or_404, render
from django.db.models.aggregates import Count, Min, Max, Avg, Sum
from django.http import HttpResponse
from store.models import Product,Customer, Order, OrderItem, Collection
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Product
from .serializer import ProductSerializer,CollectionSerializer

def say_hello(request):
    orders = Order.objects.filter(customer__id=1).aggregate(Count('id'))
    units_sold = OrderItem.objects.filter(product__id=1).aggregate(total_units_sold=Sum('quantity'))
    calculate = Product.objects.filter(collection__id=3).aggregate(min_price=Min('unit_price'), max_price=Max('unit_price'), avg_price=Avg('unit_price'))

    return render(request, 'hello.html', {'name': 'Prathik', 'result': calculate})


class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    def get_queryset(self):
        return Product.objects.select_related('collection').all()

    def get_serializer_context(self):
        return {'request':self.request}

class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def delete(self,request,pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response({'error':'Product cannot be deleted cause it is associated with OrderItem'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#-------------------------------------Collection-----------------------------------------------

class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products'))
    serializer_class = CollectionSerializer
    def delete(self,request,pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.product.count() > 0:
            return Response({'error':'Collection cannot be deleted cause it is associated with Product'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)