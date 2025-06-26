from django.contrib import admin
from .models import TTSConversion


@admin.register(TTSConversion)
class TTSConversionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'voice', 'language', 'speed', 'created_at')
    list_filter = ('status', 'voice', 'language', 'created_at')
    search_fields = ('user__username', 'user__email', 'text')
    readonly_fields = ('id', 'created_at', 'updated_at')

    fieldsets = (
        ('Basic Info', {
            'fields': ('id', 'user', 'status', 'created_at', 'updated_at')
        }),
        ('Text Info', {
            'fields': ('text', 'voice', 'language', 'speed')
        }),
        ('Audio Info', {
            'fields': ('audio_file', 'duration', 'file_size', 'error')
        }),
    )
