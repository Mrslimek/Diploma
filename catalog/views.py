# django
from django.shortcuts import render
from django.core.paginator import Paginator
# Project
from .forms import SearchForm
from .models import *
from basket.models import CartItem


def home(request):

    search_form = SearchForm()

    product_categories = ProductCategory.objects.all()
    products = Product.objects.all()
    products_by_date = products.order_by('-date_added')
    products_by_popularity = products.order_by('-popularity')
    brands = Brand.objects.all()[:12]
    articles = Article.objects.all()
    user = request.user
    cart_items_count = 0

    if user.is_authenticated:
        cart_items_count = CartItem.objects.filter(user=request.user).count()

    context = {
        'search_form': search_form,
        'categories': product_categories,
        'products_by_date': products_by_date,
        'products_by_popularity': products_by_popularity,
        'brands': brands,
        'articles': articles,
        'cart_items_count': cart_items_count
    }

    return render(request, 'Zoo.html', context)

def catalog_filter_by_id(request, product_category_id):

    search_form = SearchForm()
    
    categories = ProductCategory.objects.all()
    current_category = categories.get(id=product_category_id)
    products = Product.objects.filter(product_category=product_category_id)
    paginator = Paginator(products, 15)
    products_by_popularity = products.order_by('-popularity')
    choices = ProductType.objects.all()
    brands = Brand.objects.filter(product_category=product_category_id)
    articles = Article.objects.all()
    user = request.user
    cart_items_count = 0

    if user.is_authenticated:
        cart_items_count = CartItem.objects.filter(user=request.user).count()

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    
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
        'page_obj': page_obj,
        'cart_items_count': cart_items_count,
        'articles': articles
    }

    return render(request, 'catalogZooFilteredByCategory.html', context)

def catalog(request):

    search_form = SearchForm()

    categories = ProductCategory.objects.all()
    products = Product.objects.all()
    prods_by_popularity = products.order_by('-popularity')
    choices = ProductType.objects.all()
    brands = Brand.objects.all()
    promotion = Promotion.objects.all()
    articles = Article.objects.all()
    user = request.user
    cart_items_count = 0

    if user.is_authenticated:
        cart_items_count = CartItem.objects.filter(user=request.user).count()

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
        'page_obj': page_obj,
        'articles': articles,
        'cart_items_count': cart_items_count
    }

    return render(request, 'catalogZoo.html', context)

def card_product(request, id):

    products = Product.objects.all()
    product = products.get(id=id)

    search_form = SearchForm()
    
    products_by_popularity = products.order_by('-popularity')
    products_by_category = products.filter(product_category=product.product_category.all().first())
    articles = Article.objects.all()
    user = request.user
    cart_items_count = 0

    if user.is_authenticated:
        cart_items_count = CartItem.objects.filter(user=request.user).count()

    context = {
        'search_form': search_form,
        'product': product,
        'products_by_popularity': products_by_popularity,
        'products_by_category': products_by_category,
        'cart_items_count': cart_items_count,
        'articles': articles
        }

    return render(request, 'cardProduct.html', context)

def brands(request):

    search_form = SearchForm()

    brands = Brand.objects.all()
    user = request.user
    cart_items_count = 0

    if user.is_authenticated:
        cart_items_count = CartItem.objects.filter(user=request.user).count()

    context = {
        'search_form': search_form,
        'brands': brands,
        'cart_items_count': cart_items_count
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


def articles(request):

    search_form = SearchForm()

    products_by_popularity = Product.objects.all().order_by('-popularity')
    articles = Article.objects.all()
    categories = ProductCategory.objects.all()
    user = request.user
    cart_items_count = 0

    if user.is_authenticated:
        cart_items_count = CartItem.objects.filter(user=user).count()

    context = {
        'search_form': search_form,
        'cart_items_count': cart_items_count,
        'products_by_popularity': products_by_popularity,
        'articles': articles
    }

    return render(request, 'articles.html', context)

def sales(request):

    search_form = SearchForm()

    sales = Sale.objects.all()
    products_by_popularity = Product.objects.all().order_by('-popularity')
    user = request.user
    cart_items_count = 0

    if user.is_authenticated:
        cart_items_count = CartItem.objects.filter(user=user).count()


    context = {
        'search_form': search_form,
        'sales': sales,
        'cart_items_count': cart_items_count,
        'products_by_popularity': products_by_popularity
    }

    return render(request, 'sales.html', context)

def get_full_article(request, article_id):

    form = SearchForm()

    article = Article.objects.get(id=article_id)
    user = request.user
    cart_items_count = 0

    if user.is_authenticated:
        cart_items_count = CartItem.objects.filter(user=user).count()

    context = {
        'search_form': form,
        'article': article,
        'cart_items_count': cart_items_count
    }

    return render(request, 'full_article.html', context)

def search_products(request):

    search_form = SearchForm()

    categories = ProductCategory.objects.all()
    products = Product.objects.all()
    prods_by_popularity = products.order_by('-popularity')
    choices = ProductType.objects.all()
    brands = Brand.objects.all()
    promotion = Promotion.objects.all()
    articles = Article.objects.all()
    user = request.user
    cart_items_count = 0

    if user.is_authenticated:
        cart_items_count = CartItem.objects.filter(user=request.user).count()

    paginator = Paginator(products, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    query = request.GET.get('query')
    if query:
        search_results = Product.objects.filter(title__icontains=query)
    else:
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
        'products': search_results,
        'articles': articles,
        'cart_items_count': cart_items_count
    }

    return render(request, 'search.html', context)