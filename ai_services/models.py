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

class HealthCheckLog(models.Model):
    """Log of health check results"""
    STATUS_CHOICES = [
        ('healthy', 'Healthy'),
        ('degraded', 'Degraded'),
        ('unhealthy', 'Unhealthy'),
    ]
    
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    database_status = models.CharField(max_length=20, default='unchecked')
    openai_status = models.CharField(max_length=20, default='unchecked')
    ola_maps_status = models.CharField(max_length=20, default='unchecked')
    error_details = models.JSONField(blank=True, null=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Health Check: {self.status} at {self.timestamp}"
