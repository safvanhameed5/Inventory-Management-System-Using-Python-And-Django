from django.shortcuts import render

def home(request):
    return render(request, 'products/product_home.html')