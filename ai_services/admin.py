from django.contrib import admin
from .models import AIServiceConfig, HealthCheckLog

@admin.register(AIServiceConfig)
class AIServiceConfigAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'service_name')
    search_fields = ('service_name',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(HealthCheckLog)
class HealthCheckLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'status', 'database_status', 'openai_status', 'ola_maps_status')
    list_filter = ('status', 'database_status', 'openai_status', 'ola_maps_status')
    search_fields = ('status',)
    readonly_fields = ('timestamp',)
