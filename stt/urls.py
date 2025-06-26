from django.urls import path
from . import views


urlpatterns = [
    path('convert/', views.STTConversionCreateView.as_view(), name='stt_convert'),
    path('<uuid:pk>/', views.STTConversionDetailView.as_view(), name='stt_detail'),
    path('history/', views.STTConversionListView.as_view(), name='stt_history'),
]
