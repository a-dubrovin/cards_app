from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import gettext_lazy as _


def validate_series(value):
    if value not in range(*settings.SERIES_LIMIT):
        raise ValidationError(
            _('Series value must be in %(limit)s'),
            params={'limit': settings.SERIES_LIMIT},
        )


def validate_numbers(value):
    if value not in range(*settings.NUMBER_LIMIT):
        raise ValidationError(
            _('Number value must be in %(limit)s'),
            params={'limit': settings.NUMBER_LIMIT},
        )
