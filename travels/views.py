from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import TravelPreference, Journey, TransportationDetail
from .serializers import TravelPreferenceSerializer, JourneySerializer, TransportationDetailSerializer
from ai_services.travel_ai import TravelAIService
from ai_services.ola_api import OlaMapService

# Create your views here.

class TravelPreferenceViewSet(viewsets.ModelViewSet):
    serializer_class = TravelPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return TravelPreference.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def generate_ai_journey(self, request, pk=None):
        travel_preference = self.get_object()
        travel_ai = TravelAIService()
        ola_service = OlaMapService()
        
        # Generate AI suggestion
        suggestion = travel_ai.generate_travel_suggestion(travel_preference)
        if not suggestion:
            return Response(
                {"error": "Failed to generate travel suggestion"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
        # Create a new journey from the suggestion
        journey = Journey.objects.create(
            user=request.user,
            title=f"Trip to {travel_preference.destination}",
            description=suggestion,
            destination=travel_preference.destination,
            start_date=request.data.get('start_date'),
            end_date=request.data.get('end_date'),
            budget=request.data.get('budget', 0),
            ai_generated=True
        )
        
        # Add transportation details if coordinates are provided
        pickup_lat = request.data.get('pickup_lat')
        pickup_lng = request.data.get('pickup_lng')
        drop_lat = request.data.get('drop_lat')
        drop_lng = request.data.get('drop_lng')
        
        if all([pickup_lat, pickup_lng, drop_lat, drop_lng]):
            ride_data = ola_service.find_lowest_cost_ride(
                pickup_lat, pickup_lng, drop_lat, drop_lng
            )
            
            if ride_data:
                TransportationDetail.objects.create(
                    journey=journey,
                    pickup_location=request.data.get('pickup_location', 'Unknown'),
                    drop_location=request.data.get('drop_location', 'Unknown'),
                    pickup_lat=pickup_lat,
                    pickup_lng=pickup_lng,
                    drop_lat=drop_lat,
                    drop_lng=drop_lng,
                    vehicle_type=ride_data.get('display_name', 'Auto'),
                    estimated_cost=ride_data.get('fare_breakdown', {}).get('estimated_fare', 0)
                )
        
        return Response(JourneySerializer(journey).data)

class JourneyViewSet(viewsets.ModelViewSet):
    serializer_class = JourneySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        status_filter = self.request.query_params.get('status', None)
        queryset = Journey.objects.filter(user=self.request.user)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(detail=True, methods=['post'])
    def add_transportation(self, request, pk=None):
        journey = self.get_object()
        ola_service = OlaMapService()
        
        pickup_lat = request.data.get('pickup_lat')
        pickup_lng = request.data.get('pickup_lng')
        drop_lat = request.data.get('drop_lat')
        drop_lng = request.data.get('drop_lng')
        
        if not all([pickup_lat, pickup_lng, drop_lat, drop_lng]):
            return Response(
                {"error": "Missing location coordinates"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        ride_options = ola_service.get_ride_options(
            pickup_lat, pickup_lng, drop_lat, drop_lng
        )
        
        if not ride_options:
            return Response(
                {"error": "No ride options available"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        return Response({"ride_options": ride_options})
