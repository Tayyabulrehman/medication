from datetime import date

from django.db import transaction

from api.medicine.models import DosageTime, Medicine
from main.serilaizer import DynamicFieldsModelSerializer
from rest_framework import serializers


class DosageTimeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False)
    time = serializers.TimeField()
    taken = serializers.SerializerMethodField()

    class Meta:
        model = DosageTime
        fields = ("id", "time", "taken")

    def get_taken(self, obj):
        return True if obj.dosage_history.filter(created_on__date=date.today()).exists() else False


class MedicineSerializer(DynamicFieldsModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    remainder_time = serializers.IntegerField()
    forgot_remainder = serializers.IntegerField()
    start_from = serializers.DateField()
    quantity = serializers.IntegerField()
    medicine_dosage = DosageTimeSerializer(many=True, required=True)
    total_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Medicine
        fields = (
            "id",
            "name",
            "user_id",
            "remainder_time",
            "forgot_remainder",
            "start_from",
            "quantity",
            "medicine_dosage",
            "total_quantity"
        )

    def create(self, validated_data):
        with transaction.atomic():
            dosage = validated_data.pop("medicine_dosage")
            obj = Medicine.objects.create(**validated_data)
            DosageTime.objects.bulk_create([DosageTime(medicine_id=obj.id, time=x['time']) for x in dosage])
            return obj

    def update(self, instance, validated_data):
        with transaction.atomic():
            dosage = validated_data.pop("medicine_dosage")
            updated, creation, deleting = [], [], []
            for x in dosage:
                if x.get("id"):
                    deleting.append(x["id"])
                    updated.append(DosageTime(id=x["id"], time=x['time']))
                else:
                    creation.append(DosageTime(medicine_id=instance.id, time=x["time"]))
            if creation:
                DosageTime.objects.bulk_create(creation)
            if updated:
                DosageTime.objects.bulk_update(updated, fields=["time"])
            if deleting:
                DosageTime.objects.filter(medicine_id=instance.id).exclude(id__in=deleting).update(is_active=False)

            instance.quantity = validated_data.get('quantity', instance.quantity)
            instance.name = validated_data.get('name', instance.name)
            instance.remainder_time = validated_data.get('remainder_time', instance.remainder_time)
            instance.forgot_remainder = validated_data.get('forgot_remainder', instance.forgot_remainder)
            instance.start_from = validated_data.get('start_from', instance.start_from)
            instance.save()
            return instance

    def get_total_quantity(self, obj):
        return obj.get_quantity()

    def to_representation(self, instance):
        data = super(MedicineSerializer, self).to_representation(instance)
        data['quantity'] = data.pop('total_quantity')
        return data
