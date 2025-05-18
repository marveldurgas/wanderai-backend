from rest_framework import serializers
from .models import User, TravelPreference

class TravelPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelPreference
        fields = ('preferred_destinations', 'budget_range', 'accommodation_type', 
                  'travel_style', 'interests')

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'profile_picture', 
                  'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'profile_picture', 
                  'first_name', 'last_name', 'bio', 'date_of_birth')
        read_only_fields = ('id', 'username', 'email')

class UserDetailSerializer(serializers.ModelSerializer):
    travel_preference = TravelPreferenceSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'profile_picture',
                 'first_name', 'last_name', 'bio', 'date_of_birth',
                 'countries_visited', 'total_trips', 'total_distance',
                 'theme', 'language', 'travel_preference')
        read_only_fields = ('id', 'username', 'email')

class UserTravelStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('countries_visited', 'total_trips', 'total_distance')

class UserUIPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('theme', 'language')

class UserDataExportSerializer(serializers.ModelSerializer):
    travel_preference = TravelPreferenceSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'first_name', 'last_name', 
                 'date_joined', 'bio', 'date_of_birth', 'countries_visited', 
                 'total_trips', 'total_distance', 'travel_preference')

class SupabaseAuthSerializer(serializers.Serializer):
    supabase_uid = serializers.CharField()
    email = serializers.EmailField()
    username = serializers.CharField(required=False)
    profile_picture = serializers.URLField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    confirm_password = serializers.CharField(required=True, min_length=8)
    
    def validate_new_password(self, value):
        # Add custom password validation if needed
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        
        # Check for at least one digit
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        
        # Check for at least one uppercase letter
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        
        return value 