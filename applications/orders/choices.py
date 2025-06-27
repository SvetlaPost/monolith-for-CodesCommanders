from django.db import models

class OrderProgress(models.TextChoices):
    CREATED = 'created', 'Created'
    PROCESSING = 'processing', 'Processing'
    SHIPPING = 'shipping', 'Shipping'
    COMPLETED = 'completed', 'Completed'
