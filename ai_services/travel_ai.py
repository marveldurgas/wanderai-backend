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
        """Generate AI travel itinerary based on user preferences
        
        travel_preference can be either a TravelPreference object or a dictionary with preference data
        """
        # Handle both dictionary and object inputs
        if isinstance(travel_preference, dict):
            destination = travel_preference.get('destination', '')
            duration = travel_preference.get('duration', '')
            budget = travel_preference.get('budget', '')
            interests = travel_preference.get('interests', '')
            companion = travel_preference.get('companions', '')
            special_requirements = travel_preference.get('special_requirements', 'None')
        else:
            destination = travel_preference.destination
            duration = travel_preference.duration
            budget = travel_preference.budget
            interests = travel_preference.interests
            companion = travel_preference.companion
            special_requirements = travel_preference.special_requirements or 'None'
        
        prompt = f"""
        Generate a personalized travel itinerary based on the following preferences:
        
        Destination: {destination}
        Duration: {duration}
        Style/Budget: {budget}
        Interests and Priorities: {interests}
        Companion: {companion}
        Special Requirements: {special_requirements}
        
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
            itinerary = response.choices[0].message.content
            
            # Return structured response for frontend
            return {
                "itinerary": itinerary,
                "destination": destination,
                "duration": duration,
                "budget": budget
            }
        except Exception as e:
            print(f"Error generating travel suggestion: {str(e)}")
            raise e
    
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
            raise e 