# Generated by Django 4.2.6 on 2024-03-11 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0012_product_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default=0, upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='logo',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]
