# Generated by Django 4.2.6 on 2024-02-27 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_users_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='avatar',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=''),
        ),
    ]