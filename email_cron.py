import os
import threading
from datetime import date, datetime

import django
from django.contrib.staticfiles.storage import staticfiles_storage

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "medication.settings.base")
django.setup()
from django.db import models
from django.db.models import Q, Case, When, Value, F
from django.db.models.functions import ExtractDay
from django.utils.text import slugify

from api.calendars.models import Appointment
from api.calendars.serializer import AppointmentSerializer
from api.medicine.models import Medicine
from api.medicine.serializer import MedicineSerializer


def send_email_thread():
    t1 = threading.Thread(target=send_email())
    t1.start()


def send_email():
    try:
        s = date.today()
        query = Q(start_from__lte=date.today()) & Q(end_to__gte=s) & Q(is_active=True, )
        medi_query_set = Medicine \
            .objects \
            .filter(query) \
            .annotate(
            divisor=Case(
                When(frequency='daily', then=Value(1)),
                When(frequency='weekly', then=Value(7)),
                default=Value(30),
                output_field=models.IntegerField()
            )
        ).annotate(days=(ExtractDay(s - (F('start_from')))), )
        arr = []
        for x in medi_query_set:
            if x.days % x.divisor == 0:
                arr.append(x)

        serializer1 = MedicineSerializer(arr, many=True)
        appointment_query_set = Appointment.objects.filter(date=date.today())
        serializer2 = AppointmentSerializer(appointment_query_set, many=True)

        for x in serializer2.data:
            hour = datetime.now().hour
            min = datetime.now().min
            pass
            # if datetime.now().date() ==
        for x in serializer1.data:
            for y in x['medicine_dosage']:
                pass





    except Exception as e:
        print(e)


if __name__ == '__main__':
    send_email_thread()
