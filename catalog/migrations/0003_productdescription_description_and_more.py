# Generated by Django 5.1.3 on 2024-12-02 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_productimage_options_productdescription'),
    ]

    operations = [
        migrations.AddField(
            model_name='productdescription',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='productdescription',
            name='food_additives',
            field=models.TextField(blank=True, null=True, verbose_name='Пищевые добавки'),
        ),
        migrations.AlterField(
            model_name='productdescription',
            name='guaranteed_analysis',
            field=models.TextField(blank=True, null=True, verbose_name='Гарантированный анализ'),
        ),
        migrations.AlterField(
            model_name='productdescription',
            name='ingridients',
            field=models.TextField(blank=True, null=True, verbose_name='Состав'),
        ),
        migrations.AlterField(
            model_name='productdescription',
            name='key_features',
            field=models.TextField(blank=True, null=True, verbose_name='Ключевые особенности'),
        ),
    ]