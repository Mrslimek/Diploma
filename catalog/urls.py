from django.contrib import admin
from django.urls import include, path
from .views import (
    home, catalog, card_product, brands,
    basket, articles, RegisterView, login,
    reset_password, catalog_filter_by_id, get_products, get_products_filtered_by_type)



urlpatterns = [
    path('', home),
    path('catalog/', catalog),
    path('catalog/<int:product_category_id>', catalog_filter_by_id, name='filtered_products'),
    path('details/<int:id>', card_product, name='card_product'),
    path('brands/', brands),
    path('basket/', basket),
    path('articles/', articles),
    path('register/', RegisterView.as_view()),
    path('login/', login),
    path('reset_form/', reset_password),
    path('api/products/', get_products),
    path('api/filtered_products/', get_products_filtered_by_type),
]