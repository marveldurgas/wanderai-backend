import openai
from django.conf import settings
from .models import AIServiceConfig

class TravelAIService:
    def __init__(self):
        try:
            # Get API key from database or fallback to settings
            ai_config = AIServiceConfig.objects.get(service_name="openai", is_active=True)
            api_key = ai_config.api_key
        except AIServiceConfig.DoesNotExist:
            api_key = getattr(settings, "OPENAI_API_KEY", "")
            
        self.openai_client = openai.OpenAI(api_key=api_key)
    
    def generate_travel_suggestion(self, travel_preference):
        """Generate AI travel suggestion based on user preferences"""
        prompt = f"""
        Generate a personalized travel itinerary based on the following preferences:
        
        Destination: {travel_preference.destination}
        Duration: {travel_preference.duration}
        Style/Budget: {travel_preference.budget}
        Interests and Priorities: {travel_preference.interests}
        Companion: {travel_preference.companion}
        Special Requirements: {travel_preference.special_requirements or 'None'}
        
        Provide a detailed day-by-day itinerary with suggested activities, places to visit,
        accommodation options, and estimated costs.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert travel planner with deep knowledge of global destinations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating travel suggestion: {str(e)}")
            return None
    
    def optimize_travel_budget(self, itinerary, ola_rides_data):
        """Optimize travel budget by finding cost-effective transportation options"""
        prompt = f"""
        Optimize this travel itinerary for cost-effectiveness:
        
        Original Itinerary:
        {itinerary}
        
        Available Transportation Options:
        {ola_rides_data}
        
        Please suggest the most cost-effective and convenient transportation choices
        while maintaining the quality of the travel experience.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert in travel budget optimization."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error optimizing travel budget: {str(e)}")
            return None 