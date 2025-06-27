import re
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from applications.users.choices import UserRole
from applications.users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    role = serializers.ChoiceField(choices=UserRole.choices, required=True)
    is_staff = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password',
            're_password',
            'email',
            'role',
            'is_staff',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            're_password': {'write_only': True},
        }

    def _validate_required_field(self, value, field_name):
        if not value:
            raise serializers.ValidationError({field_name: f"{field_name.replace('_', ' ').capitalize()} is required."})

    def validate(self, attrs):
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')
        email = attrs.get('email')
        password = attrs.get('password')
        re_password = attrs.get('re_password')

        self._validate_required_field(first_name, 'first_name')
        self._validate_required_field(last_name, 'last_name')
        self._validate_required_field(email, 'email')
        self._validate_required_field(password, 'password')
        self._validate_required_field(re_password, 're_password')

        try:
            validate_email(email)
        except ValidationError:
            raise serializers.ValidationError({'email': 'Please enter a valid email address.'})

        if not first_name.isalpha():
            raise serializers.ValidationError({"first_name": "Firstname must contain only letters."})
        if not last_name.isalpha():
            raise serializers.ValidationError({"last_name": "Lastname must contain only letters."})

        validate_password(password)

        if password != re_password:
            raise serializers.ValidationError({"re_password": "Passwords do not match."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('re_password')
        role = validated_data.get('role')
        validated_data['is_staff'] = role == UserRole.ADMIN.name

        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        error_messages={
            'required': 'The username field is required.',
            'invalid': 'Enter a valid username.'
        }
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        error_messages={
            'required': 'The password field is required.',
            'min_length': 'Password must be at least 8 characters long.'
        }
    )



class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]

    def validate(self, attrs):
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')

        if not first_name or not first_name.isalpha():
            raise serializers.ValidationError({"first_name": "Firstname must contain only letters."})
        if not last_name or not last_name.isalpha():
            raise serializers.ValidationError({"last_name": "Lastname must contain only letters."})

        return attrs
