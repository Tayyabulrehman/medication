import datetime
from datetime import date

from django.conf import settings
from django.db import models
from dateutil.relativedelta import relativedelta
# Create your models here.
from api.users.models import User
from main.models import Log


class MedicineFrequency:
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'


class Remainder:
    EMAIL = 'email'
    POPUP = 'popup'


class Medicine(Log):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_medicine')
    name = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True)
    dosage_amount = models.IntegerField(null=True)
    unit = models.CharField(max_length=10, null=True)
    frequency = models.CharField(max_length=15, null=True)

    end_to = models.DateField(null=True)
    meal = models.CharField(max_length=15, null=True)
    instructions = models.TextField(null=True)
    reminders = models.CharField(max_length=20, null=True)
    image = models.ImageField(null=True)
    additional_notes = models.TextField(null=True)
    start_from = models.DateField(null=True)

    remainder_time = models.IntegerField(default=5)
    forgot_remainder = models.IntegerField(default=5)

    quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    medication_type_other = models.TextField(null=True)

    class Meta:
        db_table = 'Medicine'

    def get_quantity(self):
        return self.quantity - DosageHistory.objects.filter(dosage__medicine_id=self.id).count()

    #
    # def is_enable(self):
    #     return True if self.medicine_dosage.first().is_enable() else False


class DosageTime(Log):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True, related_name='medicine_dosage')
    time = models.TimeField(null=True)
    is_active = models.BooleanField(default=True, null=True)
    event_id = models.TextField(null=True)

    def is_taken(self):
        data = datetime.date.today()
        routine = self.medicine.frequency
        if routine == MedicineFrequency.DAILY:
            return True if self.dosage_history.filter(date=data).exists() else False
        else:
            days = 7 if self.medicine.frequency == MedicineFrequency.WEEKLY else 30
            last_dosage = self.dosage_history.last()
            if last_dosage:
                return False if last_dosage.date + datetime.timedelta(days=days) == data else True
            else:
                return False if self.medicine.start_from == data else True

    @staticmethod
    def get_un_sync_dosage():
        dic = {}
        obj = DosageTime.objects.filter(event_id__isnull=True, is_active=True, medicine__is_active=True)
        for x in obj:
            arr = []
            if x.medicine.end_to:
                days = (x.medicine.end_to - x.medicine.start_from).days
            else:
                days = x.medicine.quantity

            daye_time = datetime.datetime.combine(x.medicine.start_from, x.time)
            while days >= 0:

                a = {
                    "summary": x.medicine.name,
                    "description": x.medicine.name,
                    "start": {
                        "dateTime": daye_time.strftime('%Y-%m-%dT%H:%M:%S'),
                        "timeZone": settings.TIME_ZON
                    },
                    "end": {
                        "dateTime": daye_time.strftime('%Y-%m-%dT%H:%M:%S'),
                        "timeZone": settings.TIME_ZON
                    },
                    "location": "Event Location",
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
                arr.append(a)
                if x.medicine.frequency == MedicineFrequency.DAILY:
                    days -= 1
                    daye_time = daye_time + datetime.timedelta(days=1)

                if x.medicine.frequency == MedicineFrequency.WEEKLY:
                    daye_time = daye_time + datetime.timedelta(days=7)
                    days -= 7
                if x.medicine.frequency == MedicineFrequency.MONTHLY:
                    daye_time = daye_time + datetime.timedelta(days=30)
                    days -= 30
            dic[x.id] = arr
        return dic

    @staticmethod
    def get_total_dose_by_month():
        try:
            month = []

            data = []
            start = Medicine.objects.filter(is_active=True).order_by("start_from").first().start_from
            end = date.today()
            month.append(start)
            while start.month < end.month:
                start += relativedelta(months=1)
                month.append(start)
            for x in month:
                count = 0
                for y in Medicine.objects.filter(start_from__lte=x, end_to__gte=x, is_active=True):
                    days = 1
                    if x + datetime.timedelta(days=30) <= y.end_to:
                        days = 30
                    else:
                        days = (date.today() - y.start_from).days
                        # days =1 if days==0 else days
                    if y.frequency == MedicineFrequency.MONTHLY:
                        days = 1
                    if y.frequency == MedicineFrequency.WEEKLY:
                        days = days / 7
                    count += y.medicine_dosage.filter(is_active=True).count() * days
                data.append({
                    "month": x,
                    "c": count
                })
            return data




        except:
            return 10

    @staticmethod
    def get_total_dose_by_week():
        try:
            month = []
            data = []
            week = 1
            start = Medicine.objects.filter(is_active=True).order_by("start_from").first().start_from
            end = date.today()
            month.append(start)
            start += relativedelta(weeks=1)
            while start < end:
                start += relativedelta(weeks=1)
                month.append(start)
            for x in month:
                count = 0
                for y in Medicine.objects.filter(start_from__lte=x, end_to__gte=x, is_active=True):
                    days = 0
                    if x + datetime.timedelta(days=7) <= y.end_to:
                        days = 7
                    else:
                        days = (date.today() - y.start_from).days
                        # days = 1 if days == 0 else days
                    if y.frequency == MedicineFrequency.MONTHLY:
                        days = 0
                    if y.frequency == MedicineFrequency.WEEKLY:
                        days = 1
                    count += y.medicine_dosage.filter(is_active=True).count() * days
                data.append({
                    "week": week,
                    "c": count
                })
                week += 1
            return data




        except:
            return 10


class DosageHistory(Log):
    dosage = models.ForeignKey(DosageTime, on_delete=models.CASCADE, null=True, related_name='dosage_history')
    date = models.DateField(null=True)
