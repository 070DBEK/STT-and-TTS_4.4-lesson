import uuid
from django.db import models
from django.contrib.auth.models import User


class STTConversion(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    MODEL_CHOICES = [
        ('tiny', 'Tiny'),
        ('base', 'Base'),
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stt_conversions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    text = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=10, default='en')
    model = models.CharField(max_length=20, choices=MODEL_CHOICES, default='base')
    duration = models.FloatField(null=True, blank=True)
    file_name = models.CharField(max_length=255)
    file_size = models.IntegerField()
    audio_file = models.FileField(upload_to='stt_audio/', null=True, blank=True)
    error = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'STT Conversion'
        verbose_name_plural = 'STT Conversions'

    def __str__(self):
        return f"STT {self.id} - {self.status}"
