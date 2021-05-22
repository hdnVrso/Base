from django.urls import path
from .views import Health, Requests, RequestsHistory, RequestsRating, ResetPassword, SetEmail
urlpatterns = [
    path('health/', Health.as_view(), name='health'),
    path('requests/', Requests.as_view(), name='requests'),
    path(
        'requests/history',
        RequestsHistory.as_view(),
        name='requests_history'),
    path('requests/rating', RequestsRating.as_view(), name='requests_rating'),
    path('setEmail', SetEmail.as_view(), name='set_email'),
    path('resetPassword', ResetPassword.as_view(), name='reset_password')
]
