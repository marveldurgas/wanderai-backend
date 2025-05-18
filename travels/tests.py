from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import TravelPreference, Journey, TransportationDetail
from datetime import date, timedelta

User = get_user_model()

class TravelPreferenceModelTests(TestCase):
    """Tests for the TravelPreference model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )
        
        self.travel_preference = TravelPreference.objects.create(
            user=self.user,
            destination="Tokyo",
            duration="10 days",
            budget="High",
            interests="Technology, Food, Shopping",
            companion="Solo",
            special_requirements="Vegetarian food options"
        )
    
    def test_travel_preference_creation(self):
        self.assertEqual(self.travel_preference.destination, "Tokyo")
        self.assertEqual(self.travel_preference.duration, "10 days")
        self.assertEqual(self.travel_preference.budget, "High")
        self.assertEqual(self.travel_preference.interests, "Technology, Food, Shopping")
        self.assertEqual(self.travel_preference.companion, "Solo")
        self.assertEqual(self.travel_preference.special_requirements, "Vegetarian food options")
        self.assertEqual(self.travel_preference.user, self.user)
    
    def test_string_representation(self):
        self.assertEqual(
            str(self.travel_preference),
            f"{self.user.username}'s preference for Tokyo"
        )

class JourneyModelTests(TestCase):
    """Tests for the Journey model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )
        
        # Create a test journey
        self.start_date = date.today()
        self.end_date = self.start_date + timedelta(days=7)
        
        self.journey = Journey.objects.create(
            user=self.user,
            title="Week in Barcelona",
            description="A wonderful week exploring Barcelona",
            destination="Barcelona",
            start_date=self.start_date,
            end_date=self.end_date,
            budget=1500.00,
            status="pending",
            ai_generated=True
        )
        
        # Create transportation details
        self.transportation = TransportationDetail.objects.create(
            journey=self.journey,
            pickup_location="Barcelona Airport",
            drop_location="City Center Hotel",
            pickup_lat=41.2974,
            pickup_lng=2.0833,
            drop_lat=41.3851,
            drop_lng=2.1734,
            vehicle_type="Taxi",
            estimated_cost=35.50
        )
    
    def test_journey_creation(self):
        self.assertEqual(self.journey.title, "Week in Barcelona")
        self.assertEqual(self.journey.destination, "Barcelona")
        self.assertEqual(self.journey.start_date, self.start_date)
        self.assertEqual(self.journey.end_date, self.end_date)
        self.assertEqual(self.journey.budget, 1500.00)
        self.assertEqual(self.journey.status, "pending")
        self.assertTrue(self.journey.ai_generated)
        self.assertEqual(self.journey.user, self.user)
    
    def test_transportation_detail_creation(self):
        self.assertEqual(self.transportation.pickup_location, "Barcelona Airport")
        self.assertEqual(self.transportation.drop_location, "City Center Hotel")
        self.assertEqual(self.transportation.pickup_lat, 41.2974)
        self.assertEqual(self.transportation.pickup_lng, 2.0833)
        self.assertEqual(self.transportation.vehicle_type, "Taxi")
        self.assertEqual(self.transportation.estimated_cost, 35.50)
        self.assertEqual(self.transportation.journey, self.journey)
    
    def test_string_representations(self):
        self.assertEqual(str(self.journey), "Week in Barcelona - Barcelona")
        self.assertEqual(str(self.transportation), "Transportation for Week in Barcelona")

class TravelAPITests(APITestCase):
    """Tests for the Travel API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Create test data
        self.travel_preference = TravelPreference.objects.create(
            user=self.user,
            destination="Rome",
            duration="5 days",
            budget="Medium",
            interests="History, Food",
            companion="Couple"
        )
        
        self.start_date = date.today()
        self.end_date = self.start_date + timedelta(days=5)
        
        self.journey = Journey.objects.create(
            user=self.user,
            title="Roman Holiday",
            description="Exploring ancient Rome",
            destination="Rome",
            start_date=self.start_date,
            end_date=self.end_date,
            budget=1200.00,
            status="pending",
            ai_generated=False
        )
    
    def test_list_travel_preferences(self):
        url = '/api/travel-preferences/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['destination'], 'Rome')
    
    def test_create_travel_preference(self):
        url = '/api/travel-preferences/'
        data = {
            'destination': 'Paris',
            'duration': '7 days',
            'budget': 'High',
            'interests': 'Art, Romance',
            'companion': 'Family'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TravelPreference.objects.count(), 2)
        self.assertEqual(TravelPreference.objects.filter(destination='Paris').count(), 1)
    
    def test_list_journeys(self):
        url = '/api/journeys/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Roman Holiday')
    
    def test_filter_journeys_by_status(self):
        # Create a completed journey
        Journey.objects.create(
            user=self.user,
            title="Past Trip",
            description="A journey already taken",
            destination="Venice",
            start_date=self.start_date - timedelta(days=20),
            end_date=self.start_date - timedelta(days=15),
            budget=800.00,
            status="completed",
            ai_generated=False
        )
        
        url = '/api/journeys/?status=completed'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Past Trip')
        self.assertEqual(response.data[0]['status'], 'completed')
