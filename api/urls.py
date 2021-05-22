from django.urls import path
from .views import Health, Requests, RequestsHistory, RequestsRating, ResetPassword, SetEmail
urlpatterns = [
    path('health/', Health.as_view(), name='health'),
<<<<<<< HEAD
    path('requests/', Requests.as_view(), name='requests'),
    path(
        'requests/history',
        RequestsHistory.as_view(),
        name='requests_history'),
    path('requests/rating', RequestsRating.as_view(), name='requests_rating'),
    path('setEmail', SetEmail.as_view(), name='set_email'),
    path('resetPassword', ResetPassword.as_view(), name='reset_password')
=======
    #path('requests/', Requests.as_view(), name='requests'),
    #path(
    #    'requests/history',
    #    RequestsHistory.as_view(),
    #    name='requests_history'),
    #path('requests/rating', RequestsRating.as_view(), name='requests_rating'),
    #path('resetPassword', ResetPassword.as_view(), name='reset_password')
>>>>>>> 8d9c5e620883dff99ebd8b3331f4a8def4548540
]
