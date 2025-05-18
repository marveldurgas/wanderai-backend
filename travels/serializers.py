from rest_framework import serializers
from .models import TravelPreference, Journey, TransportationDetail, TripReview

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

class TripReviewSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = TripReview
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at', 'user_username')
    
    def validate(self, data):
        """
        Check that the user is reviewing their own journey.
        """
        user = self.context['request'].user
        journey = data.get('journey')
        
        if journey and journey.user != user:
            raise serializers.ValidationError("You can only review your own journeys.")
        
        return data

class JourneySerializer(serializers.ModelSerializer):
    transportation = TransportationDetailSerializer(many=True, read_only=True)
    reviews = TripReviewSerializer(many=True, read_only=True)
    review_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Journey
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'transportation', 'reviews', 'review_count', 'average_rating')
    
    def get_review_count(self, obj):
        return obj.reviews.count()
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return None
        return sum(review.rating for review in reviews) / reviews.count() 