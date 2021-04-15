from django.urls import path
from .views import Health, Users, Requests, RequestsHistory, RequestsRating, Tokens

urlpatterns = [
    path('health/', Health.as_view(), name='health'),
    path('users/', Users.as_view(), name='users'),
    path('requests/', Requests.as_view(), name='requests'),
    path(
        'requests/history',
        RequestsHistory.as_view(),
        name='requests_history'),
    path('requests/rating', RequestsRating.as_view(), name='requests_rating'),
    path('tokens', Tokens.as_view(), name='tokens'),
]
