import django_filters
from .models import STTConversion


class STTConversionFilter(django_filters.FilterSet):
    """Filter for STT conversions"""
    status = django_filters.ChoiceFilter(choices=STTConversion.STATUS_CHOICES)
    language = django_filters.CharFilter(lookup_expr='iexact')
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = STTConversion
        fields = ['status', 'language', 'start_date', 'end_date']
