# Generated by Django 5.1.3 on 2024-12-08 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_product_type_of_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='type_of_product',
            new_name='product_type',
        ),
    ]