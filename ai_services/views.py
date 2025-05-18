from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import AIServiceConfig
from .travel_ai import TravelAIService
from .ola_api import OlaMapService

# Create your views here.

class AIServiceView:
    """
    Non-model based view for AI services
    """
    
    @staticmethod
    def generate_travel_plan(travel_preference, user):
        """Generate a travel plan based on preferences"""
        travel_ai = TravelAIService()
        return travel_ai.generate_travel_suggestion(travel_preference)
    
    @staticmethod
    def get_transportation_options(pickup_lat, pickup_lng, drop_lat, drop_lng):
        """Get transportation options from Ola Maps API"""
        ola_service = OlaMapService()
        return ola_service.get_ride_options(pickup_lat, pickup_lng, drop_lat, drop_lng)
