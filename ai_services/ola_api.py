import requests
import json
from django.conf import settings
from .models import AIServiceConfig

class OlaMapService:
    def __init__(self):
        self.base_url = "https://devapi.olacabs.com/v1"
        
        try:
            # Get API key from database or fallback to settings
            ola_config = AIServiceConfig.objects.get(service_name="ola_maps", is_active=True)
            self.app_token = ola_config.api_key
        except AIServiceConfig.DoesNotExist:
            self.app_token = getattr(settings, "OLA_APP_TOKEN", "")
    
    def get_ride_estimate(self, pickup_lat, pickup_lng, drop_lat, drop_lng, category="auto"):
        """Get ride estimate from Ola Maps API"""
        headers = {
            "x-app-token": self.app_token,
            "Content-Type": "application/json"
        }
        
        params = {
            "pickup_lat": pickup_lat,
            "pickup_lng": pickup_lng,
            "drop_lat": drop_lat,
            "drop_lng": drop_lng,
            "service_type": "p2p",
            "category": category
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/products",
                headers=headers,
                params=params
            )
            return response.json()
        except Exception as e:
            print(f"Error fetching ride estimate: {str(e)}")
            return None
    
    def find_lowest_cost_ride(self, pickup_lat, pickup_lng, drop_lat, drop_lng):
        """Find the lowest cost ride option"""
        ride_data = self.get_ride_estimate(pickup_lat, pickup_lng, drop_lat, drop_lng)
        if not ride_data or "categories" not in ride_data:
            return None
            
        lowest_cost = float('inf')
        lowest_cost_ride = None
        
        for category in ride_data.get("categories", []):
            if "fare_breakdown" in category:
                estimated_fare = category["fare_breakdown"].get("estimated_fare", float('inf'))
                if estimated_fare < lowest_cost:
                    lowest_cost = estimated_fare
                    lowest_cost_ride = category
        
        return lowest_cost_ride
    
    def get_ride_options(self, pickup_lat, pickup_lng, drop_lat, drop_lng):
        """Get all available ride options sorted by price"""
        ride_data = self.get_ride_estimate(pickup_lat, pickup_lng, drop_lat, drop_lng)
        if not ride_data or "categories" not in ride_data:
            return []
            
        options = []
        for category in ride_data.get("categories", []):
            if "fare_breakdown" in category:
                options.append({
                    "type": category.get("display_name", "Unknown"),
                    "estimated_fare": category["fare_breakdown"].get("estimated_fare", 0),
                    "eta": category.get("eta", "Unknown"),
                    "category": category.get("id", "Unknown")
                })
        
        # Sort options by price
        return sorted(options, key=lambda x: x["estimated_fare"]) 