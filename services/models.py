from django.db import models
from App.utils.models import AppModel


class InsuranceType(models.TextChoices):
        NONLIVE = 'nonLive'
        LIVE = 'live'
        
class Products(AppModel):
    name_en = models.CharField(max_length=255)
    name_fr = models.CharField(max_length=255)
    description_en = models.TextField()
    description_fr = models.TextField()
    image = models.ImageField()
    insurance_type = models.CharFeild(choice=InsuranceType , default=InsuranceType.LIVE)


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

class Premium(AppModel):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    annuitant_amount_to_be_paid = models.DecimalField(max_digits=15, decimal_places=2)
    premium_for_guarantee = models.DecimalField(max_digits=15, decimal_places=2)
    duration = models.CharField(max_length=50)


class MedicalHistoryQuestion(AppModel):
    question_id = models.AutoField(primary_key=True)
    question_text = models.TextField()

class UserMedicalHistory(AppModel):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    question = models.ForeignKey(MedicalHistoryQuestion, on_delete=models.CASCADE)
    response = models.BooleanField()

class InsuranceQuestion(AppModel):
    question_id = models.AutoField(primary_key=True)
    question_text = models.TextField()
    insurance_service = models.CharField(max_length=255)

class EligibilityCriteria(AppModel):
    criteria_id = models.AutoField(primary_key=True)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    meets_criteria = models.BooleanField()

class Subscription(AppModel):
    subscription_id = models.AutoField(primary_key=True)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    insurance_service = models.CharField(max_length=255)
    subscription_date = models.DateField(auto_now_add=True)