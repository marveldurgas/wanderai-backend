from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import AIServiceConfig, HealthCheckLog
from .travel_ai import TravelAIService
from .ola_api import OlaMapService

# Create your views here.

class TravelAIServiceView(viewsets.ViewSet):
    """
    ViewSet for AI travel services
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def generate_travel_plan(self, request):
        """Generate a travel plan based on preferences"""
        try:
            travel_ai = TravelAIService()
            travel_plan = travel_ai.generate_travel_suggestion(request.data)
            return Response(travel_plan, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Failed to generate travel plan: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def get_transportation_options(self, request):
        """Get transportation options from Ola Maps API"""
        try:
            pickup_lat = float(request.data.get('pickup_lat'))
            pickup_lng = float(request.data.get('pickup_lng'))
            drop_lat = float(request.data.get('drop_lat'))
            drop_lng = float(request.data.get('drop_lng'))
            
            ola_service = OlaMapService()
            options = ola_service.get_ride_options(
                pickup_lat, pickup_lng, drop_lat, drop_lng
            )
            
            return Response(options, status=status.HTTP_200_OK)
        except (ValueError, KeyError) as e:
            return Response(
                {"error": f"Invalid coordinates: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to get transportation options: {str(e)}"},
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
