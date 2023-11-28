from django.db import models

from App.utils.models import AppModel

class FAQ(AppModel):
    question_en = models.TextField()
    question_fr = models.TextField()
    answer_en = models.TextField()
    answer_en = models.TextField()