# django
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.forms import ValidationError
# DRF
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Project
from .forms import RegisterForm, LoginForm, ResetForm
from .serializers import ProductSerializer, FilterProductSerializer
from .models import *

def home(request):

    product_categories = ProductCategory.objects.all()
    products = Product.objects.all()
    products_by_date = products.order_by('-date_added')
    products_by_popularity = products.order_by('-popularity')
    brands = Brand.objects.all()[:12]

    context = {
        'categories': product_categories,
        'products_by_date': products_by_date,
        'products_by_popularity': products_by_popularity,
        'brands': brands
    }

    return render(request, 'Zoo.html', context=context)

def catalog_filter_by_id(request, product_category_id):
    
    categories = ProductCategory.objects.all()
    current_category = categories.get(id=product_category_id)
    products = Product.objects.filter(product_category=product_category_id)
    paginator = Paginator(products, 15)
    products_by_popularity = products.order_by('-popularity')
    choices = ProductType.objects.all()
    brands = Brand.objects.filter(product_category=product_category_id)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    def get_category_name():
        category = categories.get(id=product_category_id)
        return category.name

    context = {
        'category_name': get_category_name,
        'current_category': current_category,
        'products': products,
        'choices': choices,
        'brands': brands,
        'categories': categories,
        'products_by_popularity': products_by_popularity,
        'page_obj': page_obj
    }

    return render(request, 'catalogZooFilteredByCategory.html', context)

def catalog(request):

    categories = ProductCategory.objects.all()
    products = Product.objects.all()
    prods_by_popularity = products.order_by('-popularity')
    choices = ProductType.objects.all()
    brands = Brand.objects.all()
    promotion = Promotion.objects.all()
    paginator = Paginator(products, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': products,
        'prods_by_popularity': prods_by_popularity,
        'choices': choices,
        'brands': brands,
        'promotion': promotion,
        'categories': categories,
        'page_obj': page_obj
    }

    return render(request, 'catalogZoo.html', context)

def card_product(request, id):

    products = Product.objects.all()
    product = products.get(id=id)
    products_by_popularity = products.order_by('-popularity')
    products_by_category = products.filter(product_category=product.product_category)

    context = {
        'product': product,
        'products_by_popularity': products_by_popularity,
        'products_by_category': products_by_category,
        }

    return render(request, 'cardProduct.html', context)

def brands(request):

    brands = Brand.objects.all()

    context = {
        'brands': brands
    }

    return render(request, 'brands.html', context)

def basket(request):
    return render(request, 'basket.html')

def articles(request):

    categories = ProductCategory.objects.all()

    return render(request, 'articles.html', {'categories': categories})

def register_user(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('http://127.0.0.1:8000/login/')
        if form.errors:
            form = form

    context = {
        'form': form
    }

    return render(request, 'register.html', context)

def login_user(request):


    form = LoginForm()

    if request.method == 'POST':
        form_data = LoginForm(data=request.POST)
        if form_data.is_valid():
            username = form_data.cleaned_data.get('username')
            password = form_data.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('http://127.0.0.1:8000/')
        else:
            form = form_data

    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/')

def reset_password(request):

    form = ResetForm()
    context = {'form': form}

    if request.method == 'POST':
        form_data = ResetForm(request.POST)
        if form_data.is_valid():
            email = form_data.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                message = 'На указанный адрес было отправлено письмо для восстановления пароля'
                context['message'] = message
            else:
                message = 'Пользователя с таким email не существует'
                context['message'] = message

    return render(request, 'reset_form.html', context)


# APIView

@api_view(['GET'])
def get_products(request):

    products = Product.objects.all()
    serializer = FilterProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def get_products_filtered(request):

    filters = {}

    product_category = request.data.get('product_category')
    product_type = request.data.get('product_type')
    promotion = request.data.get('promotion')
    brand = request.data.get('brand')
    order_by = request.data.get('order_by')

    if product_category:
        filters['product_category'] = product_category

    if product_type:
        filters['product_type_id'] = product_type
        
    if brand:
        filters['brand_id__in'] = brand

    if promotion:
        products = Product.objects.filter(**filters).filter(promotion__isnull=False)
    else:
        products = Product.objects.filter(**filters)

    if order_by:
        products = products.order_by(order_by)

    page_number = request.data.get('page_number')
    paginator = Paginator(products, 15)
    page_obj = paginator.get_page(page_number)

    serializer = FilterProductSerializer(page_obj, many=True)

    response_data = {
        "products": serializer.data,
        "has_previous": page_obj.has_previous(),
        "has_next": page_obj.has_next(),
        "previous_page_number": page_obj.previous_page_number() if page_obj.has_previous() else None,
        "next_page_number": page_obj.next_page_number() if page_obj.has_next() else None,
        "total_pages": paginator.num_pages,
        "current_page": page_number,
    }

    return Response(response_data)