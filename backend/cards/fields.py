from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class LeadingZerosField(serializers.IntegerField):
    def to_representation(self, obj):
        zeros_count = len(str(self.max_value)) if self.max_value else 0
        return str(obj).zfill(zeros_count)

    def to_internal_value(self, data):
        try:
            return int(data)
        except ValueError:
            raise ValidationError(_('Value must be integer'))
