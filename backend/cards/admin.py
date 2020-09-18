from django.contrib import admin

from .models import CardSeries, CardNumber


class CardSeriesAdmin(admin.ModelAdmin):
    pass


class CardNumberAdmin(admin.ModelAdmin):
    pass


admin.site.register(CardSeries, CardSeriesAdmin)
admin.site.register(CardNumber, CardNumberAdmin)
