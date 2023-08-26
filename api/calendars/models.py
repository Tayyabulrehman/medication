from django.db import models

# Create your models here.
from api.users.models import User
from main.models import Log
from medication.utils import GoogleCalenderManager


class Appointment(Log):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_appointment', null=True)
    title = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(null=True)
    remainder = models.IntegerField(default=5)
    event_id = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'Appointment'

    # def sava(self, *args, **kwargs):
    #     if self.user.access_token:
    #
    #             id = GoogleCalenderManager(self.user.access_token).creat_event(obj)
    #             self.event_id = id
    #         super().save()
    #     except Exception:
    #         raise

    @staticmethod
    def get_un_sync_appointment():
        obj = Appointment.objects.filter(event_id__isnull=True)
        dic = {}
        for x in obj:
            a = {
                "summary": x.title,
                "description": x.title,
                "start": {
                    "dateTime": x.date.strftime('%Y-%m-%dT%H:%M:%S'),
                    "timeZone": "America/New_York"
                },
                "end": {
                    "dateTime": x.strftime('%Y-%m-%dT%H:%M:%S'),
                    "timeZone": "America/New_York"
                },
                "location": x.location,
                # "attendees": [
                #     {"email": "attendee1@example.com"},
                #     {"email": "attendee2@example.com"}
                # ],
                "reminders": {
                    "useDefault": False,
                    "overrides": [
                        {"method": "email", "minutes": x.medicine.remainder_time},
                        {"method": "popup", "minutes": x.medicine.remainder_time}
                    ]
                }
            }
            dic[x.id] = a