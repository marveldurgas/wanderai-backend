from django.contrib import admin
from .models import TravelPreference, Journey, TransportationDetail, TripReview

@admin.register(TravelPreference)
class TravelPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'destination', 'duration', 'budget', 'created_at')
    list_filter = ('destination', 'budget')
    search_fields = ('user__username', 'destination', 'interests')
    readonly_fields = ('created_at',)

class TransportationDetailInline(admin.TabularInline):
    model = TransportationDetail
    extra = 0

@admin.register(Journey)
class JourneyAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'destination', 'start_date', 'end_date', 'status', 'ai_generated')
    list_filter = ('status', 'ai_generated', 'destination')
    search_fields = ('title', 'user__username', 'destination')
    readonly_fields = ('created_at',)
    inlines = [TransportationDetailInline]

@admin.register(TransportationDetail)
class TransportationDetailAdmin(admin.ModelAdmin):
    list_display = ('journey', 'pickup_location', 'drop_location', 'vehicle_type', 'estimated_cost')
    list_filter = ('vehicle_type',)
    search_fields = ('journey__title', 'pickup_location', 'drop_location')

@admin.register(TripReview)
class TripReviewAdmin(admin.ModelAdmin):
    list_display = ('journey', 'user', 'rating', 'created_at')
    search_fields = ('journey__title', 'user__username', 'comment')
    list_filter = ('rating', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
