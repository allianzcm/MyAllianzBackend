# Generated by Django 4.2.6 on 2024-03-11 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='zone_covered',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.RESTRICT, to='services.zonecover'),
            preserve_default=False,
        ),
    ]
