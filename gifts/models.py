from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from App .models import AppModel
User = get_user_model()

class Gifts(AppModel):
    name_en = models.CharField(max_length=30 , blank=False)
    name_fr = models.CharField(max_length=30 , blank=False)
    desc_en = models.TextField()
    desc_fr = models.TextField()
    stars = models.IntegerField()

    def __str__(self) -> str:
        return self.name_en

    class Meta:
        db_table = 'gifts'
        verbose_name = _("gift")
        verbose_name_plural = _("gifts")

class GiftRequests(AppModel):
    STATUS = [
        ('pen','pending'),
        ('app','approved'),
        ('rej','rejected'),
        ('rec','received'),
    ]
    user = models.ForeignKey(User , on_delete=models.RESTRICT )
    gift = models.ForeignKey(Gifts , on_delete=models.RESTRICT)
    
    status = models.CharField(max_length=5 , choices=STATUS , default=STATUS[0][0])
    
    def __str__(self) -> str:
        return self.gift
    
    class Meta:
        db_table = 'gift_requests'
        verbose_name = _("gift request")
        verbose_name_plural = _("gift requests")