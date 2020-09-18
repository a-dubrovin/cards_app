from django.urls import path
from rest_framework.authtoken import views

from .views import UserCreate


urlpatterns = [
    path(
        'register/',
        UserCreate.as_view(),
        name='register',
    ),
    path(
        'token/',
        views.obtain_auth_token,
        name='token',
    ),
]
