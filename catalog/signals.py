from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product

# @receiver(signal=, sender=Product, dispatch_uid='product_popularity_signal')
# def product_popularity_signal(sender, instance, created, **kwargs):
#     pass