# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, help_text='Confirm password')
    email = serializers.EmailField(required=True, allow_blank=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        # 1. Check if passwords match
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        # 2. Check if username is already taken
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "A user with that username already exists."})

        # 3. Check if email is already taken
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "This email address is already in use."})

        return data

    def create(self, validated_data):
        # Remove password2 as it's not part of the User model
        validated_data.pop('password2')

        # Create user with hashed password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user