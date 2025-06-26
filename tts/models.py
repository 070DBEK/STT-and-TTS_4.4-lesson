import uuid
from django.db import models
from django.contrib.auth.models import User


class TTSConversion(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    VOICE_CHOICES = [
        ('alloy', 'Alloy'),
        ('echo', 'Echo'),
        ('fable', 'Fable'),
        ('onyx', 'Onyx'),
        ('nova', 'Nova'),
        ('shimmer', 'Shimmer'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tts_conversions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    text = models.TextField()
    voice = models.CharField(max_length=20, choices=VOICE_CHOICES, default='alloy')
    language = models.CharField(max_length=10, default='en')
    speed = models.FloatField(default=1.0)
    duration = models.FloatField(null=True, blank=True)
    file_size = models.IntegerField(null=True, blank=True)
    audio_file = models.FileField(upload_to='tts_audio/', null=True, blank=True)
    error = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'TTS Conversion'
        verbose_name_plural = 'TTS Conversions'

    def __str__(self):
        return f"TTS {self.id} - {self.status}"

    @property
    def audio_url(self):
        if self.audio_file and self.status == 'completed':
            return self.audio_file.url
        return None
