from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'full_name', 'password', 'confirm_password', 'role']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords must match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return CustomUser.objects.create_user(**validated_data)
