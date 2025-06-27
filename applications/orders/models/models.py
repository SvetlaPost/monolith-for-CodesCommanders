from django.db import models
from django.utils import timezone

from applications.orders.models.soft_delete import SoftDeleteModel
from applications.orders.choices import OrderProgress
from applications.users.models import User


class Order(SoftDeleteModel):
    title = models.CharField(max_length=100, db_index=True)
    description = models.TextField(max_length=400)
    status = models.CharField(max_length=50, choices=OrderProgress.choices, default=OrderProgress.CREATED)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "order"
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'status', 'is_deleted'],
                name='unique_orders_title_status_not_deleted'
            )
        ]

    def __str__(self):
        return self.title