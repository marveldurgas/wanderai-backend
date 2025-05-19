"""
URL configuration for wanderlustai_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from users.views import UserViewSet
from travels.views import TravelPreferenceViewSet, JourneyViewSet, TripReviewViewSet
from ai_services.views import ai_services_health_check, generate_travel_plan
from ai_services.models import HealthCheckLog

# Setup the API router
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'travel-preferences', TravelPreferenceViewSet, basename='travel-preference')
router.register(r'journeys', JourneyViewSet, basename='journey')
router.register(r'trip-reviews', TripReviewViewSet, basename='trip-review')

# Custom health check view
def health_check(request):
    health_data = {
        'status': 'healthy',
        'services': {
            'database': 'up',
            'api': 'up',
        },
        'version': '1.0.0',
    }
    
    # Check database connection
    db_error = None
    try:
        connections['default'].cursor()
    except OperationalError as e:
        health_data['status'] = 'unhealthy'
        health_data['services']['database'] = 'down'
        db_error = str(e)
    
    # Log the health check results
    try:
        HealthCheckLog.objects.create(
            status=health_data['status'],
            database_status=health_data['services']['database'],
            error_details={} if not db_error else {'database': db_error}
        )
    except Exception as e:
        # Don't let logging failure affect the health check response
        health_data['logging_error'] = str(e)
    
    status_code = 200 if health_data['status'] == 'healthy' else 500
    return JsonResponse(health_data, status=status_code)

# API v1 endpoint patterns
api_v1_patterns = [
    # JWT authentication
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # AI Services endpoints
    path('ai_services/generate_travel_plan/', generate_travel_plan, name='generate_travel_plan'),
    
    # Include router URLs
    path('', include(router.urls)),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # API endpoints - version 1
    path('api/v1/', include(api_v1_patterns)),
    
    # Legacy API endpoints (for backward compatibility)
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair_legacy'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh_legacy'),
    
    # API documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Health checks
    path('health/', health_check, name='health_check'),
    path('health/ai/', ai_services_health_check, name='ai_health_check'),
]
