from rest_framework import serializers

from api.calendars.models import Appointment
from api.medicine.serializer import MedicineSerializer
from api.symptoms.serializer import SymptomsSerializer
from api.users.models import User


class AppointmentSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    location = serializers.CharField()
    date = serializers.DateTimeField()
    remainder = serializers.IntegerField()

    class Meta:
        model = Appointment
        fields = (
            "user_id",
            "id",
            "title",
            "location",
            "date",
            "remainder",
        )

    def create(self, validated_data):
        return Appointment.objects.create(**validated_data)

    def to_representation(self, instance):
        data = super(AppointmentSerializer, self).to_representation(instance)
        data['time'] = instance.date.strftime("%H:%M:%S")
        return data


class CalendarSerializer(serializers.ModelSerializer):
    appointment = AppointmentSerializer(read_only=True, many=True)
    symptoms = SymptomsSerializer(read_only=True, many=True)
    medicine = MedicineSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ("appointment", "symptoms", "medicine")
