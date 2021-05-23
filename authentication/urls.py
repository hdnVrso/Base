from django.urls import path

from .views import RegistrationAPIView, ObtainTokenAPIView, RefreshTokenAPIView

app_name = 'authentication'
urlpatterns = [
    path('register', RegistrationAPIView.as_view(), name='register'),
    path('tokens/obtain', ObtainTokenAPIView.as_view(), name='obtain_token'),
    path('tokens/refresh', RefreshTokenAPIView.as_view(), name='refresh_token')
]
