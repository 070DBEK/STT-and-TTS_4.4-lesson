from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import TTSConversion
from .serializers import TTSConversionSerializer, TTSConversionCreateSerializer
from .tasks import process_tts_conversion
from .filters import TTSConversionFilter


class TTSConversionCreateView(generics.CreateAPIView):
    serializer_class = TTSConversionCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversion = TTSConversion.objects.create(
            user=request.user,
            **serializer.validated_data
        )
        process_tts_conversion.delay(str(conversion.id))
        response_serializer = TTSConversionSerializer(
            conversion,
            context={'request': request}
        )
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class TTSConversionDetailView(generics.RetrieveAPIView):
    serializer_class = TTSConversionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TTSConversion.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class TTSConversionListView(generics.ListAPIView):
    serializer_class = TTSConversionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TTSConversionFilter
    search_fields = ['text']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return TTSConversion.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_tts_audio(request, pk):
    try:
        conversion = TTSConversion.objects.get(
            id=pk,
            user=request.user,
            status='completed'
        )

        if not conversion.audio_file:
            raise Http404("Audio file not found")
        response = HttpResponse(
            conversion.audio_file.read(),
            content_type='audio/mpeg'
        )
        response['Content-Disposition'] = f'attachment; filename="tts_{conversion.id}.mp3"'
        return response

    except TTSConversion.DoesNotExist:
        raise Http404("TTS conversion not found or audio not yet generated")
