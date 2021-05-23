from django.urls import path
from .views import Health, Requests, RequestsHistory, RequestsRating, ResetPassword, CeleryDataView

urlpatterns = [
    path('health/', Health.as_view(), name='health'),
    path('celery_data/', CeleryDataView.as_view(), name='celery_data'),
    # path('requests/', Requests.as_view(), name='requests'),
    # path(
    #    'requests/history',
    #    RequestsHistory.as_view(),
    #    name='requests_history'),
    # path('requests/rating', RequestsRating.as_view(), name='requests_rating'),
    # path('resetPassword', ResetPassword.as_view(), name='reset_password')
]
