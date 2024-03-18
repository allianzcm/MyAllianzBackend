# Generated by Django 4.2.6 on 2024-03-12 09:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pricing',
            name='age_range',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.RESTRICT, to='services.agerange'),
        ),
        migrations.AddField(
            model_name='pricing',
            name='duration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='services.serviceduration'),
        ),
        migrations.AddField(
            model_name='pricing',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='services.product'),
        ),
        migrations.AddField(
            model_name='pricing',
            name='zone_covered',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.RESTRICT, to='services.zonecover'),
        ),
        migrations.AddField(
            model_name='contract',
            name='approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='contract_approved_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contract',
            name='beneficial',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='services.beneficiary'),
        ),
        migrations.AddField(
            model_name='contract',
            name='canceled_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='contract_conceled_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contract',
            name='commissioned_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='contract_commissioned', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contract',
            name='pricing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='services.pricing'),
        ),
        migrations.AddField(
            model_name='contract',
            name='subscriber_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='services.subscriber'),
        ),
        migrations.AddField(
            model_name='beneficiary',
            name='subscriber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.subscriber'),
        ),
    ]
