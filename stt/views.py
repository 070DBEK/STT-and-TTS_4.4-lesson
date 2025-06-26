from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import STTConversion
from .serializers import STTConversionSerializer, STTConversionCreateSerializer
from .tasks import process_stt_conversion
from .filters import STTConversionFilter


class STTConversionCreateView(generics.CreateAPIView):
    serializer_class = STTConversionCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        audio_file = serializer.validated_data['audio']
        language = serializer.validated_data.get('language', 'en')
        model = serializer.validated_data.get('model', 'base')
        conversion = STTConversion.objects.create(
            user=request.user,
            language=language,
            model=model,
            file_name=audio_file.name,
            file_size=audio_file.size,
            audio_file=audio_file
        )
        process_stt_conversion.delay(str(conversion.id))
        response_serializer = STTConversionSerializer(conversion)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class STTConversionDetailView(generics.RetrieveAPIView):
    serializer_class = STTConversionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return STTConversion.objects.filter(user=self.request.user)


class STTConversionListView(generics.ListAPIView):
    serializer_class = STTConversionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = STTConversionFilter
    search_fields = ['text']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return STTConversion.objects.filter(user=self.request.user)
