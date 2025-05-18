from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import AIServiceConfig
from .travel_ai import TravelAIService
from unittest.mock import patch, MagicMock
from travels.models import TravelPreference

User = get_user_model()

class AIServiceConfigTests(TestCase):
    """Tests for the AIServiceConfig model"""
    
    def setUp(self):
        self.service_config = AIServiceConfig.objects.create(
            service_name="test_service",
            api_key="test_api_key",
            is_active=True
        )
    
    def test_service_config_creation(self):
        self.assertEqual(self.service_config.service_name, "test_service")
        self.assertEqual(self.service_config.api_key, "test_api_key")
        self.assertTrue(self.service_config.is_active)
        self.assertIsNotNone(self.service_config.created_at)
        self.assertIsNotNone(self.service_config.updated_at)
    
    def test_string_representation(self):
        self.assertEqual(str(self.service_config), "test_service")

class TravelAIServiceTests(TestCase):
    """Tests for the TravelAIService"""
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )
        
        # Create a test travel preference
        self.travel_preference = TravelPreference.objects.create(
            user=self.user,
            destination="Paris",
            duration="7 days",
            budget="Medium",
            interests="Art, Culture, Food",
            companion="Family"
        )
        
        # Create a service config
        self.service_config = AIServiceConfig.objects.create(
            service_name="openai",
            api_key="test_api_key",
            is_active=True
        )
    
    @patch('openai.OpenAI')
    def test_generate_travel_suggestion(self, mock_openai):
        # Mock the OpenAI client response
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        mock_completion = MagicMock()
        mock_client.chat.completions.create.return_value = mock_completion
        
        mock_choice = MagicMock()
        mock_completion.choices = [mock_choice]
        mock_choice.message.content = "This is a test itinerary for Paris."
        
        # Create the service and call the method
        service = TravelAIService()
        result = service.generate_travel_suggestion(self.travel_preference)
        
        # Check that the API was called correctly
        mock_client.chat.completions.create.assert_called_once()
        self.assertEqual(result, "This is a test itinerary for Paris.")
