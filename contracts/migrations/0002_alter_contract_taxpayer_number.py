# Generated by Django 4.2.6 on 2024-03-14 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='Taxpayer_number',
            field=models.CharField(max_length=255),
        ),
    ]