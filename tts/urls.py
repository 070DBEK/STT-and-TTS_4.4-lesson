from django.urls import path
from . import views


urlpatterns = [
    path('convert/', views.TTSConversionCreateView.as_view(), name='tts_convert'),
    path('<uuid:pk>/', views.TTSConversionDetailView.as_view(), name='tts_detail'),
    path('<uuid:pk>/audio/', views.download_tts_audio, name='tts_audio_download'),
    path('history/', views.TTSConversionListView.as_view(), name='tts_history'),
]
