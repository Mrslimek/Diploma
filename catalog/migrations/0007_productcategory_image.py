# Generated by Django 5.1.3 on 2024-12-03 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_alter_productimage_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='image',
            field=models.FileField(default='cat.png', upload_to='', verbose_name='Картинка категории'),
            preserve_default=False,
        ),
    ]
