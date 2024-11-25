from django.contrib import admin
from django.urls import include, path
from .views import home, catalog, card_product, brands, basket, articles


urlpatterns = [
    path('', home),
    path('catalog/', catalog),
    path('card_product/', card_product),
    path('brands/', brands),
    path('basket/', basket),
    path('articles/', articles),
]