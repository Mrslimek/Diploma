from django.shortcuts import render
from django.views.generic import CreateView
from .forms import RegisterForm, LoginForm, ResetForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import *

# Create your views here.

def home(request):

    product_categories = ProductCategory.objects.exclude(name='Универсальный')
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
    
    categories = ProductCategory.objects.exclude(name='Универсальный')
    products = Product.objects.filter(product_category_id=product_category_id) | Product.objects.filter(product_category_id='35')
    choices = [choice[0] for choice in Product.PRODUCT_TYPE_CHOICES]
    brands = Brand.objects.all()


    context = {
        'products': products,
        'choices': choices,
        'brands': brands,
        'categories': categories,
    }

    return render(request, 'catalogZooFiltered.html', context)

def catalog(request):

    categories = ProductCategory.objects.exclude(name='Универсальный')
    products = Product.objects.all()
    choices = [choice[0] for choice in Product.PRODUCT_TYPE_CHOICES]
    brands = Brand.objects.all()
    promotion = Promotion.objects.all()

    context = {
        'products': products,
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
    products_by_type = products.filter(product_type=product.product_type)

    context = {
        'product': product,
        'products_by_popularity': products_by_popularity,
        'products_by_type': products_by_type,
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

    categories = ProductCategory.objects.exclude(name='Универсальный')

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
