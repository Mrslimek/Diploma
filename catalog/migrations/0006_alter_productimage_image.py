# Generated by Django 5.1.3 on 2024-12-02 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_productcategory_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.FileField(upload_to='', verbose_name='Картинка продукта'),
        ),
    ]