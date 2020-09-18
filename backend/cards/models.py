import datetime

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .validators import validate_series, validate_numbers


class CardNumberManager(models.Manager):
    def cards_bulk_create(self, series, cards_quantity, end_date):
        series_obj, created = CardSeries.objects.get_or_create(series=series)
        if series_obj.available_numbers_count >= cards_quantity:
            card_obj_list = []
            for number in range(
                    series_obj.max_number + 1,
                    series_obj.max_number + cards_quantity,
            ):
                card_obj_list.append(
                    CardNumber(
                        series=series_obj,
                        number=number,
                        end_date=end_date,
                    )
                )
            self.bulk_create(card_obj_list)
        else:
            raise ValidationError(
                _('Card numbers required more than available')
            )


class CardSeries(models.Model):
    series = models.PositiveSmallIntegerField(
        verbose_name=_('Card series'),
        primary_key=True,
        validators=[validate_series],

    )

    @property
    def max_number(self):
        qs = CardNumber.objects.filter(
            series=self
        ).aggregate(
            max_number=models.Max('number')
        )
        return qs['max_number'] if qs['max_number'] else 0

    @property
    def available_numbers_count(self):
        return settings.NUMBER_LIMIT[1] - self.max_number

    def __str__(self):
        return str(self.series).zfill(settings.SERIES_DIGITS_COUNT)


class CardNumber(models.Model):
    objects = CardNumberManager()

    series = models.ForeignKey(
        CardSeries,
        on_delete=models.CASCADE,
        related_name='card_numbers',
    )
    number = models.PositiveIntegerField(
        verbose_name=_('Card number'),
        validators=[validate_numbers],
    )
    start_date = models.DateField(
        verbose_name=_('Card issue date'),
        auto_now_add=True,
    )
    end_date = models.DateField(
        verbose_name=_('Card expiration date'),
    )

    class Meta:
        unique_together = ('series', 'number')

    @property
    def is_active(self):
        now_date = datetime.datetime.now().date()
        if self.start_date <= now_date <= self.end_date:
            return True
        else:
            return False

    def __str__(self):
        return '%s %s' % (
            str(self.series).zfill(settings.SERIES_DIGITS_COUNT),
            str(self.number).zfill(settings.NUMBER_DIGITS_COUNT),
        )
