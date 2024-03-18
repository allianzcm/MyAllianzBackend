from django.db import models
from App.utils.models import AppModel


class Contract(AppModel):
    Taxpayer_number = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    big_branch = models.CharField(max_length=255)
    product = models.CharField(max_length=255)
    agent = models.CharField(max_length=255)
    date_create = models.DateField()
    effect_date = models.DateField()
    end_date = models.DateField()
    Police_number = models.CharField(max_length=255)
    amount_paid = models.IntegerField()
    company_ass = models.IntegerField()
    carrier_Acc = models.IntegerField()
    tax = models.IntegerField()
    