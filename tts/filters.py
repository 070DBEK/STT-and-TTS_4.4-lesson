import django_filters
from .models import TTSConversion


class TTSConversionFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=TTSConversion.STATUS_CHOICES)
    voice = django_filters.ChoiceFilter(choices=TTSConversion.VOICE_CHOICES)
    language = django_filters.CharFilter(lookup_expr='iexact')
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = TTSConversion
        fields = ['status', 'voice', 'language', 'start_date', 'end_date']
