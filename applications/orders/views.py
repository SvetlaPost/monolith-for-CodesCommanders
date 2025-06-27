from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from applications.orders.models.models import Order
from applications.orders.serializers import (
    OrderListSerializer,
    OrderCreateSerializer,
    OrderDetailSerializer
)
from applications.orders.permissions import IsOwnerOrReadOnly


class OrderListCreateView(ListCreateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'owner__username', 'owner__email']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        return OrderListSerializer if self.request.method in SAFE_METHODS else OrderCreateSerializer

    def get_queryset(self):
        return Order.objects.select_related('owner').filter(owner=self.request.user)

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        status_value = serializer.validated_data.get('status')

        if Order.objects.filter(title=title, status=status_value, is_deleted=False, owner=self.request.user).exists():
            raise PermissionDenied("Such order already exists.")

        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'message': 'Order created successfully',
            'data': response.data
        }, status=status.HTTP_201_CREATED)


class OrderDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    lookup_url_kwarg = 'order_id'

    def get_queryset(self):
        return Order.objects.select_related('owner')

    def get_serializer_class(self):
        return OrderDetailSerializer if self.request.method in SAFE_METHODS else OrderCreateSerializer

    def get_object(self):
        obj = super().get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied("You do not have permission to access this order.")
        return obj

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()  # soft delete
        return Response({"message": "Order deleted (soft)"}, status=status.HTTP_204_NO_CONTENT)
