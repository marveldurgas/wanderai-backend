from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
import json
from datetime import datetime
from .models import User, TravelPreference
from .serializers import (
    UserSerializer, 
    UserProfileSerializer, 
    UserDetailSerializer,
    UserTravelStatsSerializer,
    UserUIPreferencesSerializer,
    UserDataExportSerializer,
    TravelPreferenceSerializer,
    SupabaseAuthSerializer
)

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'login', 'register', 'supabase_auth']:
            return [permissions.AllowAny()]
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action == 'me':
            return UserDetailSerializer
        if self.action == 'profile':
            return UserProfileSerializer
        if self.action == 'travel_stats':
            return UserTravelStatsSerializer
        if self.action == 'preferences':
            return UserUIPreferencesSerializer
        if self.action == 'data':
            return UserDataExportSerializer
        if self.action == 'travel_preferences':
            return TravelPreferenceSerializer
        if self.action == 'supabase_auth':
            return SupabaseAuthSerializer
        return UserSerializer
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response(
            {"error": "Invalid credentials"}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """Register a new user"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.save()
            
            # Create empty travel preferences
            TravelPreference.objects.create(user=user)
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """Get or update the current user's full details"""
        user = request.user
        
        if request.method == 'GET':
            serializer = UserDetailSerializer(user)
            return Response(serializer.data)
        
        serializer = UserDetailSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def profile(self, request):
        """Manage basic profile information"""
        user = request.user
        
        if request.method == 'GET':
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)
        
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get', 'put'])
    def travel_stats(self, request):
        """Get or update user travel statistics"""
        user = request.user
        
        if request.method == 'GET':
            serializer = UserTravelStatsSerializer(user)
            return Response(serializer.data)
        
        serializer = UserTravelStatsSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def travel_stats_update(self, request):
        """Update travel stats based on completed journeys"""
        user = request.user
        
        # Example: increment countries and trips
        countries = request.data.get('countries', [])
        distance = request.data.get('distance', 0)
        
        if countries:
            user.countries_visited += len(countries)
        
        user.total_trips += 1
        user.total_distance += int(distance)
        user.save()
        
        serializer = UserTravelStatsSerializer(user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get', 'put'])
    def preferences(self, request):
        """Get or update UI preferences"""
        user = request.user
        
        if request.method == 'GET':
            serializer = UserUIPreferencesSerializer(user)
            return Response(serializer.data)
        
        serializer = UserUIPreferencesSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get', 'put'])
    def travel_preferences(self, request):
        """Get or update user travel preferences"""
        user = request.user
        
        try:
            travel_preference = TravelPreference.objects.get(user=user)
        except TravelPreference.DoesNotExist:
            travel_preference = TravelPreference.objects.create(user=user)
        
        if request.method == 'GET':
            serializer = TravelPreferenceSerializer(travel_preference)
            return Response(serializer.data)
        
        serializer = TravelPreferenceSerializer(travel_preference, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def data(self, request):
        """Export user data"""
        user = request.user
        serializer = UserDataExportSerializer(user)
        
        # Format for JSON export
        export_data = {
            'user_data': serializer.data,
            'export_date': datetime.now().isoformat()
        }
        
        return Response(export_data)
    
    @action(detail=False, methods=['post'])
    def supabase_auth(self, request):
        """Handle Supabase authentication"""
        serializer = SupabaseAuthSerializer(data=request.data)
        if serializer.is_valid():
            supabase_uid = serializer.validated_data.get('supabase_uid')
            email = serializer.validated_data.get('email')
            
            # Find or create user
            try:
                user = User.objects.get(supabase_uid=supabase_uid)
            except User.DoesNotExist:
                try:
                    # Try to find by email
                    user = User.objects.get(email=email)
                    user.supabase_uid = supabase_uid
                    user.save()
                except User.DoesNotExist:
                    # Create new user
                    username = serializer.validated_data.get('username', f"user_{supabase_uid[:8]}")
                    user = User.objects.create(
                        username=username,
                        email=email,
                        supabase_uid=supabase_uid,
                        profile_picture=serializer.validated_data.get('profile_picture', ''),
                        first_name=serializer.validated_data.get('first_name', ''),
                        last_name=serializer.validated_data.get('last_name', '')
                    )
                    # Create empty travel preferences
                    TravelPreference.objects.create(user=user)
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserDetailSerializer(user).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
