# Generated by Django 4.2.6 on 2024-01-15 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_users_verification_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='username',
        ),
        migrations.AlterField(
            model_name='users',
            name='phone',
            field=models.CharField(max_length=20),
        ),
    ]
