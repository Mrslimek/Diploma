# Generated by Django 5.1.3 on 2024-12-04 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_product_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='amount',
            field=models.IntegerField(default=1, verbose_name='Кол-во продукта'),
            preserve_default=False,
        ),
    ]