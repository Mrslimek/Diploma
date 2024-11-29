from django.contrib import admin
from django.urls import include, path
from .views import home, catalog, card_product, brands, basket, articles, RegisterView, login, reset_password



urlpatterns = [
    path('', home),
    path('catalog/', catalog),
    path('card_product/', card_product),
    path('brands/', brands),
    path('basket/', basket),
    path('articles/', articles),
    path('register/', RegisterView.as_view()),
    path('login/', login),
    path('reset_form/', reset_password)
]