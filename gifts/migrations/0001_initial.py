# Generated by Django 4.2.7 on 2023-11-28 02:25

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gift',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateField(blank=True, default=None, null=True)),
                ('name_en', models.CharField(max_length=30)),
                ('name_fr', models.CharField(max_length=30)),
                ('desc_en', models.TextField()),
                ('desc_fr', models.TextField()),
                ('img', models.ImageField(blank=True, null=True, upload_to='gifts/')),
                ('stars', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'gift',
                'verbose_name_plural': 'gifts',
                'db_table': 'gifts',
            },
        ),
        migrations.CreateModel(
            name='GiftRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateField(blank=True, default=None, null=True)),
                ('status', models.CharField(choices=[('pen', 'pending'), ('app', 'approved'), ('rej', 'rejected'), ('rec', 'received')], default='pen', max_length=5)),
                ('gift', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='gifts.gift')),
            ],
            options={
                'verbose_name': 'gift request',
                'verbose_name_plural': 'gift requests',
                'db_table': 'gift_requests',
            },
        ),
    ]
