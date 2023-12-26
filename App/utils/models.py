from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import AppManager
import uuid
from django_countries.fields import CountryField

from phonenumber_field.modelfields import PhoneNumberField


class AppModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateField(blank=True, null=True, default=None)

    objects = AppManager()
    all_objects = models.Manager()

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True


class PersonBaseModel(AppModel):
    GENDER = [
        ('m', _('male')),
        ('f', _('female')),
    ]

    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    dob = models.DateField(null=True, blank=True)
    pob = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=20)
    country = models.CharField(
        max_length=150, blank=True, null=True, default=None)
    resident = models.CharField(max_length=150, blank=True, null=True)
    phone = PhoneNumberField(null=False, blank=False)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    class Meta:
        abstract = True
