from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status
from django.urls import include, path, reverse
from django.test import TransactionTestCase


class ApiTests(APITestCase, URLPatternsTestCase, TransactionTestCase):
    urlpatterns = [
        path('api/', include('api.urls'))
    ]

    def test_endpoint_health_returns_200_ok(self):
        url = reverse('health')
        response = self.client.head(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)