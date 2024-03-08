from django.contrib.auth  import get_user_model
from django.db import models
from App.utils.models import AppModel
from services.models import Beneficiary, Subscriber

User = get_user_model()

class InsuranceType(models.TextChoices):
        NONLIVE = 'nonLive'
        LIVE = 'live'
        
class Product(AppModel):
    name_en = models.CharField(max_length=255)
    
    name_fr = models.CharField(max_length=255)

    description_en = models.TextField()

    description_fr = models.TextField()

    image = models.ImageField()

    insurance_type = models.CharFeild(choice=InsuranceType , default=InsuranceType.LIVE)


class Question(AppModel):
    question_en = models.TextField()
    question_fr = models.TextField()
    

class UserAnswer(AppModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    
    
class Subscriber(AppModel):

    class CivilStatus(models.TextChoices):

        SINGLE = 'Single'

        MARRIED = 'Married'

        DIVORCED = 'Divorced'


    civil_status = models.CharField(

        max_length=20,

        choices=CivilStatus.choices,

        default=CivilStatus.SINGLE,
    )
    
    first_name = models.CharField(max_length=255)

    last_name = models.CharField(max_length=255)

    maiden_name = models.CharField(max_length=255, blank=True, null=True)

    dob = models.DateField()

    profession = models.CharField(max_length=255)

    address = models.TextField()

    phone_number = models.CharField(max_length=20)

    id_card_number = models.CharField(max_length=50)

    email = models.EmailField()

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

    class DurationType(models.TextChoices):

        WEK = 'Weeks'

        MON = 'Months'

        YAE = 'Year'

    length = models.IntegerField()




class ZoneCover(AppModel):

    zone_en = models.TextField(max_length=200 )

    zone_fr = models.TextField(max_length=200 )
    


class AgeRange(AppModel):

    above  = models.IntegerField()

    below  = models.IntegerField()



class Pricing(AppModel):

    product = models.ForeignKey(to=Product)

    duration = models.ForeignKey(to=ServiceDuration , on_delete=models.RESTRICT)

    total_premium = models.IntegerField()

    commission = models.IntegerField()

    zone_covert = models.ForeignKey(to=ZoneCover ,on_delete=models.RESTRICT, null=True , blank=True , default=None)

    age_range = models.ForeignKey(to=AgeRange ,on_delete=models.RESTRICT, null=True , blank=True , default=None)




# This class named Contrat is a subclass of AppModel.

class Contract(AppModel):


    approved_by = models.ForeignKey(to=User , on_delete=models.RESTRICT, blank=True , null=True)
        
    approved_on = models.DateTimeField(blank=True , null=True , default=None)
    
    commissioned_by = models.ForeignKey(to=User , on_delete=models.RESTRICT , blank=True , null=True)

    subscriber_info = models.ForeignKey(to=Subscriber , on_delete=models.RESTRICT)

    pricing = models.ForeignKey(to=Pricing , on_delete=models.RESTRICT)

    beneficial = models.ForeignKey(to=Beneficiary , on_delete=models.RESTRICT , blank=True , null=True)
    