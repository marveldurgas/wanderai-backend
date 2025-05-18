from django.db import models
from users.models import User

# Create your models here.

class TravelPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='travel_preferences')
    destination = models.CharField(max_length=255)
    duration = models.CharField(max_length=100)
    budget = models.CharField(max_length=100)
    interests = models.TextField()
    companion = models.CharField(max_length=100)
    special_requirements = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s preference for {self.destination}"

class Journey(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journeys')
    title = models.CharField(max_length=255)
    description = models.TextField()
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    ai_generated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.destination}"

class TransportationDetail(models.Model):
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE, related_name='transportation')
    pickup_location = models.CharField(max_length=255)
    drop_location = models.CharField(max_length=255)
    pickup_lat = models.FloatField()
    pickup_lng = models.FloatField()
    drop_lat = models.FloatField()
    drop_lng = models.FloatField()
    vehicle_type = models.CharField(max_length=100)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2)
    ola_ride_id = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"Transportation for {self.journey.title}"

class TripReview(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Below Average'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent'),
    ]
    
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trip_reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    accommodation_rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    transportation_rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    food_rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    attractions_rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Review for {self.journey.title} by {self.user.username}"
    
    class Meta:
        unique_together = ('journey', 'user')  # One review per journey-user pair
