from django.db import models

# Create your models here.

class AIServiceConfig(models.Model):
    """Configuration for AI services"""
    service_name = models.CharField(max_length=100, unique=True)
    api_key = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.service_name
