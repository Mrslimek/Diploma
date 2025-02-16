# django
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.forms import ValidationError
# DRF
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Project
from .forms import (
    RegisterForm, LoginForm,
    ResetForm, SearchForm,
    UserProfileChangeForm, CustomUserChangeForm,
    )
from .serializers import ProductSerializer, FilterProductSerializer
from .models import *

def home(request):

    search_form = SearchForm()

    product_categories = ProductCategory.objects.all()
    products = Product.objects.all()
    products_by_date = products.order_by('-date_added')
    products_by_popularity = products.order_by('-popularity')
    brands = Brand.objects.all()[:12]
    cart_items_count = CartItem.objects.count(id=request.user)
    print(cart_item)

    context = {
        'search_form': search_form,
        'categories': product_categories,
        'products_by_date': products_by_date,
        'products_by_popularity': products_by_popularity,
        'brands': brands,
        'cart_items_count': cart_items_count
    }

    return render(request, 'Zoo.html', context=context)

def catalog_filter_by_id(request, product_category_id):

    search_form = SearchForm()
    
    categories = ProductCategory.objects.all()
    current_category = categories.get(id=product_category_id)
    products = Product.objects.filter(product_category=product_category_id)
    paginator = Paginator(products, 15)
    products_by_popularity = products.order_by('-popularity')
    choices = ProductType.objects.all()
    brands = Brand.objects.filter(product_category=product_category_id)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    print('РАБОТАЕТ PRODUCT_CATEGORY_BY_ID')

    
    def get_category_name():
        category = categories.get(id=product_category_id)
        return category.name

    context = {
        'search_form': search_form,
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

    search_form = SearchForm()

    categories = ProductCategory.objects.all()
    products = Product.objects.all()
    product_properties = []
    prods_by_popularity = products.order_by('-popularity')
    choices = ProductType.objects.all()
    brands = Brand.objects.all()
    promotion = Promotion.objects.all()
    paginator = Paginator(products, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'search_form': search_form,
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

    search_form = SearchForm()
    
    products_by_popularity = products.order_by('-popularity')
    products_by_category = products.filter(product_category=product.product_category.all().first())
    print(products_by_category, 'PRODUCTS_BY_CATEGORY')

    context = {
        'search_form': search_form,
        'product': product,
        'products_by_popularity': products_by_popularity,
        'products_by_category': products_by_category,
        }

    return render(request, 'cardProduct.html', context)

def brands(request):

    search_form = SearchForm()

    brands = Brand.objects.all()

    context = {
        'search_form': search_form,
        'brands': brands
    }

    return render(request, 'brands.html', context)


    print(brand_id, 'BRAND_ID')

    products = Product.objects.filter(brand=brand_id)
    paginator = Paginator(products, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, 'catalogZoo.html', context)

def basket(request):

    search_form = SearchForm()

    products = Product.objects.all()
    products_by_popularity = products.order_by('-popularity')
    products_by_date = products.order_by('-date_added')
    cart_products = CartItem.objects.filter(user=request.user)
    # print(cart_products[0].calculate_final_price(), 'ФИНАЛЬНАЯ ЦЕНА')
    

    context = {
        'search_form': search_form,
        'products_by_popularity': products_by_popularity,
        'products_by_date': products_by_date,
        'cart_products': cart_products
    }

    return render(request, 'basket.html', context)

def articles(request):

    search_form = SearchForm()

    categories = ProductCategory.objects.all()

    context = {
        'search_form': search_form
    }

    return render(request, 'articles.html', context)

def register_user(request):

    search_form = SearchForm()
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('http://127.0.0.1:8000/login/')
        if form.errors:
            form = form

    context = {
        'search_form': search_form,
        'form': form
    }

    return render(request, 'register.html', context)

def login_user(request):

    search_form = SearchForm()
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
    
    context = {
        'form': form,
        'search_form': search_form
        }

    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/')

def reset_password(request):

    search_form = SearchForm()
    form = ResetForm()
    context = {
        'form': form,
        'search_form': search_form
        }

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

def search_products(request):

    search_form = SearchForm()

    categories = ProductCategory.objects.all()
    products = Product.objects.all()
    prods_by_popularity = products.order_by('-popularity')
    choices = ProductType.objects.all()
    brands = Brand.objects.all()
    promotion = Promotion.objects.all()
    paginator = Paginator(products, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    query = request.GET.get('query')
    print(query)
    if query:
        search_results = Product.objects.filter(title__icontains=query)
        print(search_results, 'ПРОШЛО ПРОВЕРКУ')
    else:
        print(search_results, 'НЕ ПРОШЛО ПРОВЕРКУ')
        message = 'По вашему запросу ничего не найдено'
        search_results = Product.objects.all()

    context = {
        'search_form': search_form,
        'products': products,
        'prods_by_popularity': prods_by_popularity,
        'choices': choices,
        'brands': brands,
        'promotion': promotion,
        'categories': categories,
        'page_obj': page_obj,
        'products': search_results
    }

    return render(request, 'search.html', context)

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product, defaults={'quantity': 1})
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    # Перенаправление на ту же страницу 
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def increase_quantity(request, cart_item_id):

    product = CartItem.objects.get(id=cart_item_id)
    product.quantity += 1
    product.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/')) 

def decrease_quantity(request, cart_item_id):

    product = CartItem.objects.get(id=cart_item_id)
    product.quantity -= 1
    product.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def remove_cart_product(request, cart_item_id):

    product = CartItem.objects.get(id=cart_item_id)
    product.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def profile(request):

    user_change_form = CustomUserChangeForm()
    user_profile_change_form = UserProfileChangeForm()

    if request.method == 'POST':
        if 'user_change' in request.POST:
            user = request.user
            form_data = CustomUserChangeForm(request.POST)
            if form_data.is_valid():
                for key, value in form_data.cleaned_data.items():
                    if value:
                        setattr(user, key, value)
                        user.save()
                return render(request,'profile.html',context = {
                                                                'user_change_form': user_change_form,
                                                                'user_profile_change_form': user_profile_change_form,
                                                                'message_user': 'Данные успешно сохранены'
                                                            })      


        if 'profile_change' in request.POST:
            user_profile = UserProfile.objects.get(user=request.user)
            form_data = UserProfileChangeForm(request.POST)
            if form_data.is_valid():
                if form_data.cleaned_data['phone_number']:
                    user_profile.phone_number = form_data.cleaned_data['phone_number']
                if form_data.cleaned_data['date_of_birth']:
                    user_profile.date_of_birth = form_data.cleaned_data['date_of_birth']
                user_profile.save()
                return render(request, 'profile.html', context = {
                                                                 'user_change_form': user_change_form,
                                                                 'user_profile_change_form': user_profile_change_form,
                                                                 'message_profile': 'Данные успешно сохранены'
                                                             }) 

    context = {
        'user_change_form': user_change_form,
        'user_profile_change_form': user_profile_change_form,
    }

    return render(request, 'profile.html', context)

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