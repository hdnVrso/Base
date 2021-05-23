from django.urls import path, include
from .views import Health

urlpatterns = [
    path('api/', include('api.urls')),
    path('api/', include('authentication.urls'))
]
