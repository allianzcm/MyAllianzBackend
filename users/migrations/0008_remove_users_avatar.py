# Generated by Django 4.2.6 on 2024-02-27 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_users_username_alter_users_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='avatar',
        ),
    ]
