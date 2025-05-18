from django.contrib import admin
from .models import AIServiceConfig

@admin.register(AIServiceConfig)
class AIServiceConfigAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'service_name')
    search_fields = ('service_name',)
    readonly_fields = ('created_at', 'updated_at')
