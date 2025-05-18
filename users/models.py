from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    # Travel stats
    countries_visited = models.PositiveIntegerField(default=0)
    total_trips = models.PositiveIntegerField(default=0)
    total_distance = models.PositiveIntegerField(default=0, help_text=_("Total distance traveled in kilometers"))
    
    # UI preferences
    theme = models.CharField(max_length=20, default='light', choices=[
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('system', 'System'),
    ])
    language = models.CharField(max_length=10, default='en', choices=[
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('de', 'German'),
        ('hi', 'Hindi'),
    ])
    
    # External auth
    supabase_uid = models.CharField(max_length=255, blank=True, null=True, unique=True)
    
    def __str__(self):
        return self.username

class TravelPreference(models.Model):
    """User travel preferences model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='travel_preference')
    preferred_destinations = models.JSONField(default=list, blank=True)
    budget_range = models.CharField(max_length=50, blank=True, null=True)
    accommodation_type = models.CharField(max_length=50, blank=True, null=True)
    travel_style = models.CharField(max_length=50, blank=True, null=True, 
                                    choices=[
                                        ('luxury', 'Luxury'),
                                        ('budget', 'Budget'),
                                        ('adventure', 'Adventure'),
                                        ('cultural', 'Cultural'),
                                        ('relaxation', 'Relaxation'),
                                    ])
    interests = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Travel Preferences"
