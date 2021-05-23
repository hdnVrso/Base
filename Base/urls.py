from django.urls import path, include
from .views import Health

urlpatterns = [
    path('health', Health.as_view()),
    path('api/', include('authentication.urls'))
]
