from rest_framework import serializers
from .models import TravelPreference, Journey, TransportationDetail

class TravelPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelPreference
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

class TransportationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportationDetail
        fields = '__all__'
        read_only_fields = ('journey',)

class JourneySerializer(serializers.ModelSerializer):
    transportation = TransportationDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = Journey
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'ai_generated') 