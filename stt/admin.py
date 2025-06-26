from django.contrib import admin
from .models import STTConversion


@admin.register(STTConversion)
class STTConversionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'language', 'model', 'file_name', 'created_at')
    list_filter = ('status', 'language', 'model', 'created_at')
    search_fields = ('user__username', 'user__email', 'text', 'file_name')
    readonly_fields = ('id', 'created_at', 'updated_at')

    fieldsets = (
        ('Basic Info', {
            'fields': ('id', 'user', 'status', 'created_at', 'updated_at')
        }),
        ('Audio Info', {
            'fields': ('file_name', 'file_size', 'audio_file', 'duration')
        }),
        ('Processing Info', {
            'fields': ('language', 'model', 'text', 'error')
        }),
    )
