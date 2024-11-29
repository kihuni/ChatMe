from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)
    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = [
            'email', 'username', 'full_name',
            'password', 'confirm_password', 'role'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords must match."})
        return data

    def create(self, validated_data):
        # Remove confirm_password before creating user
        validated_data.pop('confirm_password')

        # Set default role if not provided
        if 'role' not in validated_data:
            default_role = Role.objects.get_or_create(name='member')[0]
            validated_data['role'] = default_role

        user = CustomUser.objects.create_user(**validated_data)
        return user