# Generated by Django 4.2.6 on 2024-01-02 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0004_alter_gift_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='giftrequest',
            name='validated_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='gifts.giftrequest'),
            preserve_default=False,
        ),
    ]
