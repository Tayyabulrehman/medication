from django.db import models

# Create your models here.
from api.users.models import User
from main.models import Log


class Medicine(Log):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_medicine')
    name = models.CharField(max_length=255, null=True)
    remainder_time = models.IntegerField(default=5)
    forgot_remainder = models.IntegerField(default=5)
    start_from = models.DateField(null=True)
    quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'Medicine'

    def get_quantity(self):
        return self.quantity - DosageHistory.objects.filter(dosage__medicine_id=self.id).count()


class DosageTime(Log):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True, related_name='medicine_dosage')
    time = models.TimeField(null=True, unique=True)
    is_active = models.BooleanField(default=True, null=True)


class DosageHistory(Log):
    dosage = models.ForeignKey(DosageTime, on_delete=models.CASCADE, null=True, related_name='dosage_history')
