from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path(
        'api/v1/account/',
        include(('users.urls', 'users'), namespace='users_api')
    ),
    path(
        'api/v1/',
        include(('cards.urls', 'cards'), namespace='cards_api')
    ),
    path('admin/', admin.site.urls),
]
