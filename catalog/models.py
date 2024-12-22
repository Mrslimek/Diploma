from django.db import models
from django.contrib.auth.models import User


class Brand(models.Model):

    name = models.CharField(max_length=255, unique=True, verbose_name='Название продукта')
    image = models.FileField(verbose_name='Картинка бренда')
    product_category = models.ManyToManyField('ProductCategory', verbose_name='Категория продукта')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Брэнд'
        verbose_name_plural = 'Брэнды'


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Категория продукта')
    image = models.FileField(verbose_name='Картинка категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категория товаров'


class ProductType(models.Model):
    name = models.CharField(max_length=255, verbose_name='Тип продукта')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тип продукта'
        verbose_name_plural = 'Типы продуктов'


class Product(models.Model):
    UNIT_CHOICES = [('кг', 'кг'), ('л', 'л'), ('г', 'г'), ('шт', 'шт')]
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, verbose_name='Бренд')
    title = models.CharField(max_length=255, unique=True, verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    amount = models.IntegerField(verbose_name='Кол-во продукта')
    unit = models.CharField(max_length=255, choices=UNIT_CHOICES, verbose_name='Единица измерения')
    product_type = models.ForeignKey('ProductType', on_delete=models.CASCADE, verbose_name='Тип продукта', null=True)
    product_category = models.ManyToManyField('ProductCategory', verbose_name='Категория продукта')
    date_added = models.DateTimeField(verbose_name='Дата добавления продукта', null=True)
    popularity = models.IntegerField(verbose_name='Популярность продукта', default=0)

    def price_with_discount(self):
        promotions = self.promotion_set.all()
        if promotions.exists():
            discount = promotions.first().discount
            final_price = round(self.price - (self.price * discount / 100), 2)
            return final_price

        return self.price

    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class ProductDescription(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    description = models.TextField(null=True, verbose_name= 'Описание', blank=True)
    key_features = models.TextField(null=True, verbose_name='Ключевые особенности', blank=True)
    ingridients = models.TextField(null=True, verbose_name='Состав', blank=True)
    guaranteed_analysis = models.TextField(null=True, verbose_name='Гарантированный анализ', blank=True)
    food_additives = models.TextField(null=True, verbose_name='Пищевые добавки', blank=True)

    def __str__(self):
        return f'{self.product}'

    class Meta:
        verbose_name = 'Описание продукта'
        verbose_name_plural = 'Описание продуктов'



class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт')
    image = models.FileField(verbose_name='Картинка продукта')

    def __str__(self):
        return f'{self.product} --- {self.image}'

    class Meta:
        verbose_name = 'Картинка продукта'
        verbose_name_plural = 'Картинки продуктов'


class ProductProperties(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт')
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Вес')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', default=0.00)

    def __str__(self):
        return f'{self.product} --- {self.weight} --- {self.price}'

    class Meta:
        verbose_name = 'Расфасовка продукта'
        verbose_name_plural = 'Расфасовка продуктов'


class Promotion(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Цена со скидкой')
    start_date = models.DateTimeField(verbose_name='Дата начала акции')
    end_date = models.DateTimeField(verbose_name='Дата окончания акции')


    def is_active(self):
        from django.utils import timezone
        return self.start_date <= timezone.now() <= self.end_date

    def __str__(self):
        return f'{self.product} --- {self.discount}'
    
    class Meta:
        verbose_name = 'Акционный товар'
        verbose_name_plural = 'Акционные товары'