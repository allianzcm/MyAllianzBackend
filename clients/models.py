from django.db import models
from App.utils.models import AppModel

# Create your models here.

class Client(AppModel):
    Taxpayer_number = models.CharField(max_length=255,unique=True)
    civil_status = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)