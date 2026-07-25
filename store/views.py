from django.shortcuts import get_object_or_404, render
from django.db.models.aggregates import Count, Min, Max, Avg, Sum
from django.http import HttpResponse
from store.models import Product,Customer, Order, OrderItem, Collection,Reviews
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .models import Product
from .serializer import ProductSerializer,CollectionSerializer,ReviewSerializer

def say_hello(request):
    orders = Order.objects.filter(customer__id=1).aggregate(Count('id'))
    units_sold = OrderItem.objects.filter(product__id=1).aggregate(total_units_sold=Sum('quantity'))
    calculate = Product.objects.filter(collection__id=3).aggregate(min_price=Min('unit_price'), max_price=Max('unit_price'), avg_price=Avg('unit_price'))

    return render(request, 'hello.html', {'name': 'Prathik', 'result': calculate})


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
            return {'request':self.request}

    def destroy(self,request,*args,**kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error':'Product cannot be deleted cause it is associated with OrderItem'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request,*args,**kwargs)    
    
#-------------------------------------Collection-----------------------------------------------

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def destory(self,request,*args,**kwargs):
        if Product.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error':'Collection cannot be deleted cause it is associated with Product'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request,*args,**kwargs)

#--------------------------Reviews----------------------------------------

class ReviewViewSet(ModelViewSet):
     query = Reviews.objects.all()
     serialzer_class = ReviewSerializer
