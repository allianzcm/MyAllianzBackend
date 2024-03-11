from django.contrib.auth  import get_user_model
from django.db import models
from App.utils.models import AppModel

User = get_user_model()

INSURANCE_TYPE = [
    ('nonLive' , "NON_LIVE"),
    ('live','LIVE')   
    ]

CIVIL_STATUS = [
        ("Single","SINGLE"),
        ("Married","MARRIED" ),
        ("Divorced","DIVORCED")
]    


class ZoneCover(AppModel):
    zone_en = models.CharField(max_length=200 )
    zone_fr = models.CharField(max_length=200 )
    def __str__(self):
        return self.zone_en
    
    
class Product(AppModel):
    name_en = models.CharField(max_length=255)
    name_fr = models.CharField(max_length=255)
    description_en = models.TextField()
    description_fr = models.TextField()
    image = models.ImageField(blank=True, null=True)
    insurance_type = models.CharField(max_length=20,choices=INSURANCE_TYPE)
    stars = models.IntegerField()
    # zone_covered = models.ForeignKey(ZoneCover , on_delete=models.RESTRICT , null=True,blank=True)
    def __str__(self) -> str:
        return self.name_en
class Question(AppModel):
    question_en = models.TextField()
    question_fr = models.TextField()
    

class UserAnswer(AppModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    
    
class Subscriber(AppModel):
    civil_status = models.CharField(max_length=20,choices=CIVIL_STATUS)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    maiden_name = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField()
    profession = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    id_card_number = models.CharField(max_length=50)
    email = models.EmailField()
    direct_subscription = models.BooleanField(default=True)
    unique_identification_number = models.CharField(max_length=50)

class Beneficiary(AppModel):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    age = models.IntegerField()
    address = models.TextField()
    town_resident = models.CharField(max_length=255)
    annuity_manager_phone_number = models.CharField(max_length=20)
    annuity_amount = models.DecimalField(max_digits=15, decimal_places=2)


class  ServiceDuration(AppModel):
    DURATION_TYPE = [
        ("WEK",'Weeks'),
        ("MON",'Months'),
        ("YEA",'Year')
        ]
    duration_unit =  models.CharField(max_length=5 , choices=DURATION_TYPE)
    length = models.IntegerField()
    


class AgeRange(AppModel):
    above  = models.IntegerField(null=True , blank=True)
    below  = models.IntegerField(null=True , blank=True)
    def __str__(self) -> str:
        if self.above:
            return f'> {self.above}'
        if self.below:
            return f'< {self.below}'


class Pricing(AppModel):
    product = models.ForeignKey(to=Product, on_delete=models.RESTRICT)
    duration = models.ForeignKey(to=ServiceDuration , on_delete=models.RESTRICT)
    total_premium = models.IntegerField()
    commission = models.IntegerField()
    zone_covert = models.ForeignKey(to=ZoneCover ,on_delete=models.RESTRICT, null=True , blank=True , default=None)
    age_range = models.ForeignKey(to=AgeRange ,on_delete=models.RESTRICT, null=True , blank=True , default=None)

class Contract(AppModel):
    approved_by = models.ForeignKey(to=User , on_delete=models.RESTRICT, blank=True , null=True , related_name="contract_approved_by")
    approved_on = models.DateTimeField(blank=True , null=True , default=None)
    commissioned_by = models.ForeignKey(to=User , on_delete=models.RESTRICT , blank=True , null=True , related_name="contract_commissioned")
    subscriber_info = models.ForeignKey(to=Subscriber , on_delete=models.RESTRICT)
    pricing = models.ForeignKey(to=Pricing , on_delete=models.RESTRICT)
    beneficial = models.ForeignKey(to=Beneficiary , on_delete=models.RESTRICT , blank=True , null=True)
    canceled_at = models.DateField(blank=True, null=True, default=None)
    canceled_by = models.ForeignKey(to=User , on_delete=models.RESTRICT, blank=True , null=True , related_name="contract_conceled_by")