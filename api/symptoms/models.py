from django.db import models

# Create your models here.
from api.users.models import User
from main.models import Log


class Symptoms(Log):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_symptoms', db_column='UserId')
    description = models.TextField(db_column='Description', null=True)
    severity = models.CharField(max_length=255, db_column='Severity', null=True)
    time = models.TimeField(null=True)
    date = models.DateField(null=True)
    duration = models.TextField(null=True)
    associated_factors = models.TextField(null=True)
    medications_taken = models.TextField(null=True)
    notes = models.TextField(null=True)
    triggers = models.TextField(null=True)
    body_part = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'Symptoms'
