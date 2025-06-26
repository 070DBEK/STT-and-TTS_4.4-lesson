from rest_framework import serializers
from .models import TTSConversion


class TTSConversionSerializer(serializers.ModelSerializer):
    audio_url = serializers.SerializerMethodField()
    class Meta:
        model = TTSConversion
        fields = ('id', 'status', 'text', 'voice', 'language', 'speed',
                  'duration', 'file_size', 'audio_url', 'created_at',
                  'updated_at', 'error')
        read_only_fields = ('id', 'status', 'duration', 'file_size',
                            'audio_url', 'created_at', 'updated_at', 'error')

    def get_audio_url(self, obj):
        if obj.audio_file and obj.status == 'completed':
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.audio_file.url)
        return None


class TTSConversionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TTSConversion
        fields = ('text', 'voice', 'language', 'speed')

    def validate_text(self, value):
        if len(value) > 5000:
            raise serializers.ValidationError(
                "Text exceeds maximum length of 5000 characters"
            )
        return value

    def validate_speed(self, value):
        if not (0.25 <= value <= 4.0):
            raise serializers.ValidationError(
                "Speed must be between 0.25 and 4.0"
            )
        return value
