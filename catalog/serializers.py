from rest_framework import serializers
from .models import *  


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name']


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id']


class ProductPropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductProperties
        fields = ['id', 'weight', 'price']


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'


class FilterProductSerializer(serializers.ModelSerializer):
    productimage_set = ProductImageSerializer(many=True)
    productproperties_set = ProductPropertiesSerializer(many=True)
    promotion_set = PromotionSerializer(many=True)
    brand = BrandSerializer()
    product_category = ProductCategorySerializer()
    product_type = ProductTypeSerializer()
    class Meta:
        model = Product
        fields = ['brand', 'title', 'price', 'amount',
            'unit', 'product_type', 'product_category',
            'productimage_set', 'productproperties_set',
            'promotion_set', 'date_added', 'popularity',]