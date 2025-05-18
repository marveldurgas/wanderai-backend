from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import TravelPreference, Journey, TransportationDetail, TripReview
from .serializers import TravelPreferenceSerializer, JourneySerializer, TransportationDetailSerializer, TripReviewSerializer
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
        """Generate AI journey from travel preference"""
        preference = self.get_object()
        
        travel_ai = TravelAIService()
        ai_suggestion = travel_ai.generate_travel_suggestion(preference)
        
        if not ai_suggestion:
            return Response(
                {"error": "Failed to generate travel suggestion"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
        # Parse dates from request or use defaults
        try:
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')
            budget = float(request.data.get('budget', 1000))
            
            # Create a new journey with AI suggestion
            journey_data = {
                'user': request.user,
                'title': f"Trip to {preference.destination}",
                'description': ai_suggestion,
                'destination': preference.destination,
                'start_date': start_date,
                'end_date': end_date,
                'budget': budget,
                'ai_generated': True
            }
            
            journey = Journey.objects.create(**journey_data)
            return Response(JourneySerializer(journey).data, status=status.HTTP_201_CREATED)
            
        except (ValueError, KeyError) as e:
            return Response(
                {"error": f"Invalid request data: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

class JourneyViewSet(viewsets.ModelViewSet):
    serializer_class = JourneySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Journey.objects.filter(user=self.request.user)
        
        # Filter by status if provided
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
            
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(detail=True, methods=['post'])
    def add_transportation(self, request, pk=None):
        """Add transportation details to journey"""
        journey = self.get_object()
        
        try:
            serializer = TransportationDetailSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(journey=journey)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"Failed to add transportation: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def optimize_transportation(self, request, pk=None):
        """Optimize transportation for the journey"""
        journey = self.get_object()
        transportation = journey.transportation.all()
        
        if not transportation:
            return Response(
                {"error": "No transportation details found for this journey"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        ola_service = OlaMapService()
        
        try:
            # Get ride options for all transportation segments
            optimization_data = []
            
            for transport in transportation:
                ride_options = ola_service.get_ride_options(
                    transport.pickup_lat, 
                    transport.pickup_lng,
                    transport.drop_lat,
                    transport.drop_lng
                )
                
                if ride_options:
                    optimization_data.append({
                        "segment": f"From {transport.pickup_location} to {transport.drop_location}",
                        "current_vehicle": transport.vehicle_type,
                        "current_cost": float(transport.estimated_cost),
                        "options": ride_options
                    })
            
            # If we have data to optimize, pass to AI service
            if optimization_data:
                travel_ai = TravelAIService()
                optimized_plan = travel_ai.optimize_travel_budget(
                    journey.description,
                    optimization_data
                )
                
                return Response({
                    "journey": JourneySerializer(journey).data,
                    "optimization_data": optimization_data,
                    "optimized_plan": optimized_plan
                })
            else:
                return Response({"error": "No ride options found"}, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            return Response(
                {"error": f"Optimization failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class TripReviewViewSet(viewsets.ModelViewSet):
    serializer_class = TripReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # For GET requests, users can see all reviews
        if self.request.method in permissions.SAFE_METHODS:
            # Filter by journey if journey_id is provided
            journey_id = self.request.query_params.get('journey_id')
            if journey_id:
                return TripReview.objects.filter(journey_id=journey_id)
            return TripReview.objects.all()
        
        # For other methods, users can only access their own reviews
        return TripReview.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_reviews(self, request):
        """Get all reviews by the current user"""
        reviews = TripReview.objects.filter(user=request.user)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def journey_reviews(self, request):
        """Get all reviews for a specific journey"""
        journey_id = request.query_params.get('journey_id')
        if not journey_id:
            return Response(
                {"error": "journey_id parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        journey = get_object_or_404(Journey, id=journey_id)
        reviews = TripReview.objects.filter(journey=journey)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)
