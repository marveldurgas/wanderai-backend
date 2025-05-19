from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import AIServiceConfig, HealthCheckLog
from .travel_ai import TravelAIService
from .ola_api import OlaMapService
from travels.models import TravelPreference

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

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def generate_travel_plan(request):
    """
    Generate a travel plan based on user preferences and integrate with Ola Maps API 
    for transportation options.
    """
    try:
        # Create a temporary travel preference from the request data
        preference_data = request.data.copy()
        preference_data['user'] = request.user.id
        
        # Either use existing preference or create a temporary one for processing
        preference_id = preference_data.get('id')
        if preference_id:
            travel_preference = TravelPreference.objects.get(
                id=preference_id, 
                user=request.user
            )
        else:
            # Create temporary preference object without saving to DB
            travel_preference = TravelPreference(
                user=request.user,
                destination=preference_data.get('destination', ''),
                duration=preference_data.get('duration', ''),
                budget=preference_data.get('budget', ''),
                interests=preference_data.get('interests', ''),
                companion=preference_data.get('companion', ''),
                special_requirements=preference_data.get('special_requirements', '')
            )
        
        # Generate AI travel plan
        travel_ai = TravelAIService()
        travel_plan = travel_ai.generate_travel_suggestion(travel_preference)
        
        if not travel_plan:
            return Response(
                {"error": "Failed to generate travel plan"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
        # Get transportation options if location coordinates are provided
        transportation_options = []
        if all(coord in preference_data for coord in ['pickup_lat', 'pickup_lng', 'drop_lat', 'drop_lng']):
            ola_service = OlaMapService()
            transportation_options = ola_service.get_ride_options(
                float(preference_data.get('pickup_lat')),
                float(preference_data.get('pickup_lng')),
                float(preference_data.get('drop_lat')),
                float(preference_data.get('drop_lng'))
            )
            
            # If we have transport options, optimize the plan
            if transportation_options:
                optimized_plan = travel_ai.optimize_travel_budget(
                    travel_plan,
                    transportation_options
                )
                if optimized_plan:
                    travel_plan = optimized_plan
        
        return Response({
            "travel_plan": travel_plan,
            "transportation_options": transportation_options
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"error": f"Travel plan generation failed: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def ai_services_health_check(request):
    """
    Check the health of AI services including OpenAI and Ola Maps API.
    """
    health_data = {
        'status': 'healthy',
        'services': {
            'openai': 'unchecked',
            'ola_maps': 'unchecked',
        },
        'errors': {}
    }
    
    # Check OpenAI API
    try:
        travel_ai = TravelAIService()
        # Simple prompt to test API connection
        test_response = travel_ai.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a health check assistant."},
                {"role": "user", "content": "Return only the word 'healthy' if you can read this."}
            ],
            max_tokens=10
        )
        openai_response = test_response.choices[0].message.content.strip().lower()
        if 'healthy' in openai_response:
            health_data['services']['openai'] = 'up'
        else:
            health_data['services']['openai'] = 'degraded'
            health_data['errors']['openai'] = 'Unexpected response from API'
    except Exception as e:
        health_data['status'] = 'degraded'
        health_data['services']['openai'] = 'down'
        health_data['errors']['openai'] = str(e)
    
    # Check Ola Maps API
    try:
        ola_service = OlaMapService()
        # Test with sample coordinates (Mumbai coordinates)
        test_response = ola_service.get_ride_estimate(
            pickup_lat=19.0760, 
            pickup_lng=72.8777, 
            drop_lat=19.1136, 
            drop_lng=72.9070
        )
        
        if test_response and isinstance(test_response, dict):
            health_data['services']['ola_maps'] = 'up'
        else:
            health_data['services']['ola_maps'] = 'degraded'
            health_data['errors']['ola_maps'] = 'Unexpected response format'
    except Exception as e:
        health_data['status'] = 'degraded'
        health_data['services']['ola_maps'] = 'down'
        health_data['errors']['ola_maps'] = str(e)
    
    # Update overall status
    if 'down' in health_data['services'].values():
        health_data['status'] = 'unhealthy'
    elif 'degraded' in health_data['services'].values():
        health_data['status'] = 'degraded'
    
    # Log health check results to database
    try:
        HealthCheckLog.objects.create(
            status=health_data['status'],
            openai_status=health_data['services']['openai'],
            ola_maps_status=health_data['services']['ola_maps'],
            error_details=health_data['errors'] if health_data['errors'] else None
        )
    except Exception as e:
        # Don't let logging failure affect the health check response
        health_data['logging_error'] = str(e)
    
    status_code = 200 if health_data['status'] == 'healthy' else 500 if health_data['status'] == 'unhealthy' else 200
    return Response(health_data, status=status_code)
