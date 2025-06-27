from rest_framework import serializers

from applications.orders.choices import OrderProgress
from applications.orders.models.models import Order
from applications.users.models import User


class OrderListSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'title',
            'status',
            'status_display',
            'created_at',
            'owner_username'
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'title',
            'description',
            'status'
        ]

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value

    def validate_status(self, value):
        valid_statuses = [choice[0] for choice in OrderProgress.choices]
        if value not in valid_statuses:
            raise serializers.ValidationError("Invalid status value.")
        return value


class OrderDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'title',
            'description',
            'status',
            'status_display',
            'created_at',
            'updated_at',
            'owner_username',
            'owner_email'
        ]
