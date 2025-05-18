from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import User

class UserModelTests(TestCase):
    """Tests for the custom User model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
            phone_number="+1234567890",
            profile_picture="https://example.com/profile.jpg"
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.phone_number, "+1234567890")
        self.assertEqual(self.user.profile_picture, "https://example.com/profile.jpg")
        self.assertTrue(self.user.check_password("testpassword"))
    
    def test_string_representation(self):
        self.assertEqual(str(self.user), "testuser")

class UserAPITests(APITestCase):
    """Tests for the User API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
            phone_number="+1234567890"
        )
        self.client = APIClient()
        
        # Create a second user for tests
        self.user2 = User.objects.create_user(
            username="anotheruser",
            email="another@example.com",
            password="anotherpassword"
        )
    
    def test_login(self):
        url = '/api/token/'
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_login_with_wrong_credentials(self):
        url = '/api/token/'
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_user_profile(self):
        # Authenticate the client
        self.client.force_authenticate(user=self.user)
        
        url = '/api/users/me/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['phone_number'], '+1234567890')
    
    def test_update_profile(self):
        # Authenticate the client
        self.client.force_authenticate(user=self.user)
        
        url = '/api/users/me/'
        data = {
            'phone_number': '+9876543210',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh user from database
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone_number, '+9876543210')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
    
    def test_register_user(self):
        url = '/api/users/'
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username='newuser').count(), 1)
        
        # Check the user can login
        url = '/api/token/'
        data = {
            'username': 'newuser',
            'password': 'newpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
