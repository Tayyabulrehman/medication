import datetime
from datetime import date

from django.db import models
from django.db.models import Q, F, Case, When, Value, Sum, Count
from django.db.models.functions import ExtractDay, TruncMonth
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from django.db.models.functions import ExtractWeekDay
from api.calendars.models import Appointment
from api.calendars.serializer import AppointmentSerializer
from api.medicine.models import Medicine, DosageTime, DosageHistory
from api.medicine.serializer import MedicineSerializer
from api.permissions import IsOauthAuthenticatedCustomer
from api.views import BaseAPIView
from medication.utils import search_array_of_dict


class DashboardView(BaseAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsOauthAuthenticatedCustomer, ]

    def get(self, request):
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
            total = Medicine.objects.filter(is_active=True).aggregate(medi=Sum('quantity'))['medi']
            taken = DosageTime.objects.filter(is_active=True, medicine__is_active=True).count()

            # Monthly
            taken_monthly = DosageHistory. \
                objects.filter(dosage__medicine__is_active=True). \
                annotate(month=TruncMonth('date')) \
                .values('month') \
                .annotate(c=Count('id')) \
                .values('month', 'c')
            taken_weekly = DosageHistory.objects.filter(dosage__medicine__is_active=True) \
                .annotate(week=ExtractWeekDay('date')) \
                .values('week') \
                .annotate(c=Count('id')) \
                .values('week', 'c')

            total_by_month = DosageTime.get_total_dose_by_month()
            total_by_week = DosageTime.get_total_dose_by_week()
            monthly = []
            weekly = []
            for x in total_by_month:
                s = search_array_of_dict(taken_monthly, 'month', x['month'], is_month=True)
                t = 0
                if s:
                    t = s['c']
                monthly.append(
                    {
                        "month": x['month'],
                        "taken": t,
                        "missed": 0 if x["c"] - t < 0 else x["c"] - t < 0
                    }
                )
                for x in total_by_week:
                    s = search_array_of_dict(taken_weekly, 'week', x['week'], is_month=False)
                    t = 0
                    if s:
                        t = s['c']
                    weekly.append(
                        {
                            "week": x['week'],
                            "taken": t,
                            "missed": 0 if x["c"] - t < 0 else x["c"] - t
                        }
                    )
            # for x, y in zip(total_by_week, taken_weekly):
            #     monthly.append(
            #         {
            #             "week": y['weekday'],
            #             "taken": y['c'],
            #             "missed": x["c"] - y['c']
            #         }
            #     )
            return self.send_response(
                success=True,
                status_code=status.HTTP_200_OK,
                payload={
                    "appointment": serializer2.data,
                    "medicine": serializer1.data,
                    "taken": taken,
                    "pending": total - taken,
                    "monthly": monthly,
                    "weekly": weekly
                }
            )



        except Exception as e:
            return self.send_response(
                success=False,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                description=str(e)
            )
