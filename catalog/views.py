from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'Zoo.html')

def catalog(request):
    return render(request, 'catalogZoo.html')

def card_product(request):
    return render(request, 'cardProduct.html')

def brands(request):
    return render(request, 'brands.html')

def basket(request):
    return render(request, 'basket.html')

def articles(request):
    return render(request, 'articles.html')