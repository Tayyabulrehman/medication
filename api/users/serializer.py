from rest_framework import serializers

from api.users.models import User, AccessLevel, Role
from main.serilaizer import DynamicFieldsModelSerializer


class AuthenticateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(required=True, allow_blank=False, allow_null=False)

    class Meta:
        model = User
        fields = ('email', 'password')


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    password = serializers.CharField(write_only=True, required=True, allow_null=False, allow_blank=False)
    date_of_birth = serializers.DateField()
    blood_group = serializers.CharField()
    allergies = serializers.CharField()
    emergency_contact = serializers.CharField()
    medical_condition = serializers.CharField()

    class Meta:
        model = User
        fields = (
            "first_name", "last_name", "email", "password", 'date_of_birth', 'blood_group', 'emergency_contact',
            'medical_condition', 'allergies')

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(
            **validated_data,
            role=Role.get_role_by_code(AccessLevel.CUSTOMER_CODE),
            is_active=True,
        )
        #  to track history of user
        user.set_password(password)
        user.save(update_fields=["password"])
        return user


# class UserUpdateProfileSerializer(serializers.ModelSerializer):
#     role = serializers.CharField(source='role.code', read_only=True)
#     is_active = serializers.BooleanField(read_only=True)
#     first_name = serializers.CharField(required=True, allow_blank=True, allow_null=True)
#     last_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     is_email_verified = serializers.BooleanField(read_only=True)
#
#     class Meta:
#         model = User
#         fields = ('id', 'first_name', 'last_name', 'role', "is_active", 'is_email_verified')
#
#     def update(self, instance, validated_data):
#         instance.first_name = validated_data.get('first_name', instance.first_name)
#         instance.last_name = validated_data.get('last_name', instance.last_name)
#         instance.save()
#         return instance

# def get_role(self, obj):
#     try:
#         return obj.role.name
#     except:
#         return ''


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(read_only=True)

    email = serializers.EmailField(read_only=True)
    role = serializers.CharField(source='role.code')
    is_active = serializers.BooleanField(read_only=True)

    date_of_birth = serializers.DateField()
    blood_group = serializers.CharField()
    allergies = serializers.CharField()
    emergency_contact = serializers.CharField()
    medical_condition = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'first_name',"last_name", "email", 'role', 'is_active', "is_email_verified", "is_approved",
                  "date_of_birth", 'blood_group', 'allergies', 'emergency_contact', 'medical_condition'
                  ]

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.city = validated_data.get('city', instance.city)
        instance.save()
        return instance
