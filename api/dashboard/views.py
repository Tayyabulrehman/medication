import datetime
from datetime import date

from django.db import models
from django.db.models import Q, F, Case, When, Value
from django.db.models.functions import ExtractDay
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from api.calendars.models import Appointment
from api.calendars.serializer import AppointmentSerializer
from api.medicine.models import Medicine
from api.medicine.serializer import MedicineSerializer
from api.permissions import IsOauthAuthenticatedCustomer
from api.views import BaseAPIView


class DashboardView(BaseAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsOauthAuthenticatedCustomer, ]

    def get(self, request):
        try:
            s = date.today()
            query = Q(start_from__gte=date.today()) & Q(end_to__lte=s) & Q(is_active=True, )
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
            return self.send_response(
                success=True,
                status_code=status.HTTP_200_OK,
                payload={
                    "appointment": serializer2.data,
                    "medicine": serializer1.data
                }
            )



        except Exception as e:
            return self.send_response(
                success=False,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                description=str(e)
            )
