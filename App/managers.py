from django.db import models
from django.middleware.csrf import CsrfViewMiddleware
class AppManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)