from django.contrib import admin
from . models import (Product , Question , UserAnswer ,Subscriber , Beneficiary , ServiceDuration ,  ZoneCover , AgeRange ,Pricing , Contract  )
# Register your models here.
admin.site.register(Product)
admin.site.register(Question)
admin.site.register(UserAnswer)
admin.site.register(Subscriber)
admin.site.register(Beneficiary)
admin.site.register(ServiceDuration)
admin.site.register(ZoneCover)
admin.site.register(AgeRange)
admin.site.register(Pricing)
admin.site.register(Contract)