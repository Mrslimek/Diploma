from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductCategory)
admin.site.register(ProductProperties)
admin.site.register(Promotion)
admin.site.register(Brand)
admin.site.register(ProductDescription)
admin.site.register(ProductType)
admin.site.register(UserProfile)
admin.site.register(FavouriteProduct)
admin.site.register(CartItem)
admin.site.register(Article)