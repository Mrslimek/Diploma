from django.shortcuts import render
from django.views.generic import CreateView
from .forms import RegisterForm, LoginForm, ResetForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import *
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer, FilterProductSerializer
from django.core.paginator import Paginator
 
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

    context = {
        'products': products,
        'prods_by_popularity': prods_by_popularity,
        'choices': choices,
        'brands': brands,
        'promotion': promotion,
        'categories': categories,
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

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login/')

    def form_valid(self, form):
        # Создаем пользователя
        user = form.save(commit=False)  # Не сохраняем сразу
        user.set_password(form.cleaned_data['password'])  # Устанавливаем зашифрованный пароль
        user.save()  # Сохраняем пользователя в базе данных

        return super().form_valid(form)  # Возвращаем результат родительского метода

    def form_invalid(self, form):
        # Если форма невалидна, возвращаем стандартный ответ
        return super().form_invalid(form)

def login(request):

    form = LoginForm()

    if request.method == 'POST':
        form_data = LoginForm(data=request.POST)
        

    return render(request, 'login.html', {'form': form})

def reset_password(request):

    form = ResetForm()

    if request.method == 'POST':
        form_data = ResetForm(request.POST)

    return render(request, 'reset_form.html', {'form': form})


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