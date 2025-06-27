from django.db import models

class UserRole(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    MODERATOR = 'moderator', 'Moderator'
    USER = 'user', 'User'
