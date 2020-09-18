from django.conf import settings
from rest_framework import serializers

from .fields import LeadingZerosField
from .models import CardSeries, CardNumber


class SeriesSerializer(serializers.ModelSerializer):
    series = LeadingZerosField(
        min_value=settings.SERIES_LIMIT[0],
        max_value=settings.SERIES_LIMIT[1],
    )

    class Meta:
        model = CardSeries
        fields = (
            'series',
            'max_number',
            'available_numbers_count',
        )
        read_only_fields = fields


class CardSerializer(serializers.ModelSerializer):
    series = LeadingZerosField(
        min_value=settings.SERIES_LIMIT[0],
        max_value=settings.SERIES_LIMIT[1],
    )
    number = LeadingZerosField(
        min_value=settings.NUMBER_LIMIT[0],
        max_value=settings.NUMBER_LIMIT[1],
    )

    class Meta:
        model = CardNumber
        fields = (
            'series',
            'number',
            'is_active',
            'start_date',
            'end_date',
        )
        read_only_fields = fields


class CreateCardsSerializer(serializers.Serializer):
    series = LeadingZerosField(
        min_value=settings.SERIES_LIMIT[0],
        max_value=settings.SERIES_LIMIT[1],
    )
    cards_quantity = serializers.IntegerField(
        min_value=settings.NUMBER_LIMIT[0],
        max_value=settings.NUMBER_LIMIT[1],
    )
    # Card validity in months
    validity = serializers.ChoiceField(
        choices=(
            (1, '1 month'),
            (6, '6 month'),
            (12, '1 year'),
            (36, '3 years'),
        )
    )
