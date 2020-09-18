from django.urls import path

from .views import SeriesDetailView, CardListView


urlpatterns = [
    path(
        'series/<int:series>/',
        SeriesDetailView.as_view(),
        name='series',
    ),
    path(
        'cards/',
        CardListView.as_view(),
        name='cards',
    ),
]
