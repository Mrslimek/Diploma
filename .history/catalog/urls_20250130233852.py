from django.contrib import admin
from django.urls import include, path
from .views import (
    home, catalog, card_product, brands,
    basket, articles, register_user, login_user,
    reset_password, catalog_filter_by_id,
    logout_user, search_products,
    profile, add_to_cart,
    increase_quantity, decrease_quantity,
    remove_cart_product, get_full_article,
    sales)



urlpatterns = [
    path('', home),
    path('profile/', profile, name='profile'),
    path('catalog/', catalog, name='catalog'),
    path('catalog/<int:product_category_id>', catalog_filter_by_id, name='filtered_products'),
    path('details/<int:id>', card_product, name='card_product'),
    path('brands/', brands, name='brands'),
    path('basket/', basket, name='basket'),
    path('articles/', articles, name='articles'),
    path('full_article/<int:article_id>', get_full_article, name='full_article'),
    path('results/', search_products, name='search_results'),
    path('sales/', sales, name='sales'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('reset_form/', reset_password, name='reset'),
    path('add_to_cart/<int:product_id>', add_to_cart, name='add_to_cart'),
    path('increase/<int:cart_item_id>', increase_quantity, name='increase_quantity'),
    path('decrease/<int:cart_item_id>', decrease_quantity, name='decrease_quantity'),
    path('remove/<int:cart_item_id>', remove_cart_product, name='remove_cart_product'),
]