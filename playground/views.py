from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# Request hanndling function

def say_hello(request):
    return HttpResponse("Hello World")