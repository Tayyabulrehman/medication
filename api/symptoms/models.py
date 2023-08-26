from django.db import models

# Create your models here.
from api.users.models import User
from main.models import Log


class Symptoms(Log):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_symptoms', db_column='UserId')
    title = models.CharField(max_length=255, null=True)
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
    factor_other = models.CharField(max_length=255, null=True)
    triger_other = models.CharField(max_length=255, null=True)
    event_id = models.TextField(max_length=255, null=True)

    class Meta:
        db_table = 'Symptoms'

    @staticmethod
    def get_un_sync_appointment():
        obj = Symptoms.objects.filter(event_id__isnull=True)
        dic = {}
        for x in obj:
            a = {
                "summary": x.title,
                "description": x.title,
                "start": {
                    "dateTime": x.datetime.datetime.combine(x.date, x.time).strftime('%Y-%m-%dT%H:%M:%S'),
                    "timeZone": "America/New_York"
                },
                "end": {
                    "dateTime": x.datetime.datetime.combine(x.date, x.time).strftime('%Y-%m-%dT%H:%M:%S'),
                    "timeZone": "America/New_York"
                },
                "location": "",
                # "attendees": [
                #     {"email": "attendee1@example.com"},
                #     {"email": "attendee2@example.com"}
                # ],
                "reminders": {
                    "useDefault": False,
                    "overrides": [
                        {"method": "email", "minutes": 10},
                        {"method": "popup", "minutes": 10}
                    ]
                }
            }
            dic[x.id] = a
