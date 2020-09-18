import datetime

from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from rest_framework import generics, status
from rest_framework.response import Response

from .models import CardSeries, CardNumber
from .serializers import (
    SeriesSerializer,
    CardSerializer,
    CreateCardsSerializer,
)


class SeriesDetailView(generics.RetrieveAPIView):
    serializer_class = SeriesSerializer
    lookup_field = 'series'
    queryset = CardSeries.objects.all()


class CardListView(generics.ListAPIView):
    serializer_class = CardSerializer
    queryset = CardNumber.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateCardsSerializer
        return CardSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreateCardsSerializer(
            data=request.data,
            *args,
            **kwargs
        )
        serializer.is_valid(raise_exception=True)
        now_date = datetime.datetime.now().date()
        months = serializer.validated_data['validity']
        end_date = now_date + relativedelta(months=+months)
        try:
            CardNumber.objects.cards_bulk_create(
                series=serializer.validated_data['series'],
                cards_quantity=serializer.validated_data['cards_quantity'],
                end_date=end_date
            )
            status_code = status.HTTP_201_CREATED
            message = None
        except ValidationError as e:
            status_code = status.HTTP_400_BAD_REQUEST
            message = {
                'cards_quantity': (e.message, )
            }

        return Response(
            message,
            status=status_code,
        )
