from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название продукта')
    image = models.FileField(verbose_name='Картинка бренда')

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


class Product(models.Model):
    UNIT_CHOICES = [('кг', 'кг'), ('л', 'л'), ('г', 'г'), ('шт', 'шт')]
    PRODUCT_TYPE_CHOICES = [
        ('Влажный корм', 'Влажный корм'), ('Сухой корм', 'Сухой корм'),
        ('Игрушки', 'Игрушки'), ('Переноски', 'Переноски'),
        ('Посуда', 'Посуда'), ('Клетки', 'Клетки'),
        ('Впитывающий наполнитель', 'Впитывающий наполнитель'), ('Древесный наполнитель', 'Древесный наполнитель'),
        ('Комкующийся наполнитель', 'Комкующийся наполнитель')]
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True, verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    amount = models.IntegerField(verbose_name='Кол-во продукта')
    unit = models.CharField(max_length=255, choices=UNIT_CHOICES, verbose_name='Единица измерения')
    product_type = models.CharField(max_length=255, choices=PRODUCT_TYPE_CHOICES, verbose_name='Тип продукта')
    product_category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE)
    date_added = models.DateTimeField(verbose_name='Дата добавления продукта', null=True)

    def price_with_discount(self):
        promotions = self.promotion_set.all()
        if promotions.exists():
            discount = promotions.first().discount
            final_price = round(self.price - (self.price * discount / 100), 2)
            print(final_price)
            return final_price

        return self.price

    def __str__(self):
        return f'{self.title} --- {self.product_category}'
    
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
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    image = models.FileField(verbose_name='Картинка продукта')

    def __str__(self):
        return f'{self.product} --- {self.image}'

    class Meta:
        verbose_name = 'Картинка продукта'
        verbose_name_plural = 'Картинки продуктов'


class ProductProperties(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Вес')

    def __str__(self):
        return f'{self.product} --- {self.weight}'

    class Meta:
        verbose_name = 'Расфасовка продукта'
        verbose_name_plural = 'Расфасовка продуктов'


class Promotion(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def is_active(self):
        from django.utils import timezone
        return self.start_date <= timezone.now() <= self.end_date

    def __str__(self):
        return f'{self.product} --- {self.discount}'
    
    class Meta:
        verbose_name = 'Акционный товар'
        verbose_name_plural = 'Акционные товары'