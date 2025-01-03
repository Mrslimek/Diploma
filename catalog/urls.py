from django.contrib import admin
from django.urls import include, path
from .views import (
    home, catalog, card_product, brands,
    basket, articles, register_user, login_user,
    reset_password, catalog_filter_by_id,
    get_products, get_products_filtered,
    logout_user)



urlpatterns = [
    path('', home),
    path('catalog/', catalog),
    path('catalog/<int:product_category_id>', catalog_filter_by_id, name='filtered_products'),
    path('details/<int:id>', card_product, name='card_product'),
    path('brands/', brands),
    path('basket/', basket),
    path('articles/', articles),
    path('register/', register_user),
    path('login/', login_user),
    path('logout/', logout_user),
    path('reset_form/', reset_password),
    path('api/products/', get_products),
    path('api/filtered_products/', get_products_filtered),
]