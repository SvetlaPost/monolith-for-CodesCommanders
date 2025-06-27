from django.urls import path
from applications.orders.views import (
    OrderListCreateView,
    OrderDetailView,
)

urlpatterns = [
    path('', OrderListCreateView.as_view(), name='order-list-create'),
    path('<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
]
