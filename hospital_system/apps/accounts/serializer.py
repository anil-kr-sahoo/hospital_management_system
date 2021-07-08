from rest_framework import serializers

from .models import UserSystem, USER_SYSTEM_DETAILS
from ..doctor.models import Doctor
from ..hospital.models import Hospital


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSystem
        fields = USER_SYSTEM_DETAILS

    def validate(self, data):
        email = data.get('email')
        phone_no = data.get('phone_number')
        if phone_no and len(phone_no) not in [10, 13]:
            raise serializers.ValidationError("Provide a valid phone number")
        if not (email or phone_no):
            raise serializers.ValidationError("Email or Phone number is required")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)

    class Meta:
        model = UserSystem
        fields = ['email', 'password']


class InsertionSerializer(serializers.Serializer):
    logged_email = serializers.EmailField(allow_blank=True, required=False)
    role = serializers.CharField(max_length=1, allow_blank=False, required=True)
    phone_number = serializers.CharField(max_length=13, allow_blank=True, required=False)

    class Meta:
        fields = ['role', 'logged_email', 'logged_phone']

    def validate(self, data):
        role = data.get('role')
        ref_email = data.get('logged_email')
        ref_phone = data.get('logged_phone')
        if role in ['2', '3'] and not (ref_email or ref_phone):
            raise serializers.ValidationError("logged_email or logged_phone required for role 2 and 3")
        if role == '2':
            try:
                if ref_email:
                    Hospital.objects.get(email=ref_email)
                if ref_phone:
                    Hospital.objects.get(email=ref_phone)
            except Exception as e:
                raise serializers.ValidationError("Not found any Hospital relation, "
                                                  "please provide logged_email or logged_phone of Hospital instance.")
        if role == '3':
            try:
                if ref_email:
                    doctor = Doctor.objects.get(email=ref_email)
                    hospital = doctor.hospital
                    if not hospital:
                        raise serializers.ValidationError("Not found any Hospital relation, "
                                                          "please provide logged_email or logged_phone of a doctor"
                                                          " with registered Hospital instance.")
                if ref_phone:
                    doctor = Doctor.objects.get(email=ref_phone)
                    hospital = doctor.hospital
                    if not hospital:
                        raise serializers.ValidationError("Not found any Hospital relation, "
                                                          "please provide logged_email or logged_phone of a doctor"
                                                          " with registered Hospital instance.")
            except Exception as e:
                raise serializers.ValidationError("Not found any Doctor relation, "
                                                  "please provide logged_email or logged_phone of Doctor instance.")
        return data
