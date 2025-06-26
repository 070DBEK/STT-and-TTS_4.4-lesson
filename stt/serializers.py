from rest_framework import serializers
from .models import STTConversion


class STTConversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = STTConversion
        fields = ('id', 'status', 'text', 'language', 'model', 'duration',
                  'file_name', 'file_size', 'created_at', 'updated_at', 'error')
        read_only_fields = ('id', 'status', 'text', 'duration', 'file_name',
                            'file_size', 'created_at', 'updated_at', 'error')


class STTConversionCreateSerializer(serializers.Serializer):
    audio = serializers.FileField()
    language = serializers.CharField(max_length=10, default='en')
    model = serializers.ChoiceField(
        choices=STTConversion.MODEL_CHOICES,
        default='base'
    )

    def validate_audio(self, value):
        if value.size > 26214400:
            raise serializers.ValidationError(
                "Audio file exceeds maximum size limit of 25MB"
            )
        allowed_formats = ['mp3', 'wav', 'm4a', 'mp4', 'mpeg', 'mpga', 'webm']
        file_extension = value.name.split('.')[-1].lower()

        if file_extension not in allowed_formats:
            raise serializers.ValidationError(
                f"Unsupported file format. Supported formats: {', '.join(allowed_formats)}"
            )
        return value
